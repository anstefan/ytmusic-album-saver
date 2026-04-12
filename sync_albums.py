import email
import imaplib
import os
import re
import ssl
from email.header import decode_header, make_header
from html import unescape
from typing import Optional, Tuple

from bs4 import BeautifulSoup
from ytmusicapi import OAuthCredentials, YTMusic


GMAIL_HOST = "imap.gmail.com"
GMAIL_USER = os.environ["GMAIL_USER"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
GMAIL_QUERY = os.getenv("GMAIL_QUERY", "label:album-release is:unread")

YT_CLIENT_ID = os.environ["YT_CLIENT_ID"]
YT_CLIENT_SECRET = os.environ["YT_CLIENT_SECRET"]
YTMUSIC_AUTH_FILE = os.getenv("YTMUSIC_AUTH_FILE", "oauth.json")

MIN_MATCH_SCORE = int(os.getenv("MIN_MATCH_SCORE", "5"))


def log(msg: str) -> None:
    print(msg, flush=True)


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"\(.*?\)|\[.*?\]", " ", text)
    text = re.sub(
        r"\b(deluxe|expanded|remaster|remastered|anniversary|edition|version|explicit)\b",
        " ",
        text,
    )
    text = re.sub(r"[^a-z0-9]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def decode_subject(raw_subject: str) -> str:
    if not raw_subject:
        return ""
    try:
        return str(make_header(decode_header(raw_subject)))
    except Exception:
        return raw_subject


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    return unescape(soup.get_text("\n"))


def extract_email_text(msg) -> str:
    subject = decode_subject(msg.get("Subject", ""))
    parts = [f"SUBJECT: {subject}"]

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in disposition.lower():
                continue
            try:
                payload = part.get_payload(decode=True)
                if not payload:
                    continue
                charset = part.get_content_charset() or "utf-8"
                decoded = payload.decode(charset, errors="replace")
                if content_type == "text/plain":
                    parts.append(decoded)
                elif content_type == "text/html":
                    parts.append(html_to_text(decoded))
            except Exception:
                continue
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            decoded = payload.decode(charset, errors="replace")
            if msg.get_content_type() == "text/html":
                parts.append(html_to_text(decoded))
            else:
                parts.append(decoded)

    text = "\n".join(parts)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def clean_capture(value: str) -> str:
    value = value.strip().strip("-–:|,.; ")
    value = value.strip("\"'\u201c\u201d")
    return value


def extract_artist_album(text: str) -> Tuple[Optional[str], Optional[str]]:
    patterns = [
        r'(?im)^(?P<artist>[^:\n]{2,80})\s*[-–:]\s*["\u201c](?P<album>[^"\n\u201d]{2,120})["\u201d]\s*(?:is out now|out now|new album|album release)?\s*$',
        r'(?im)^new album from\s+(?P<artist>[^\n:]{2,80})[:\s-]+["\u201c]?(?P<album>[^\n"\u201d]{2,120})["\u201d]?\s*$',
        r'(?im)^(?P<artist>[^\n]{2,80})\s+released\s+["\u201c](?P<album>[^"\n\u201d]{2,120})["\u201d]',
        r'(?is)\b(?P<artist>[A-Z0-9][A-Za-z0-9 &+!\'\-.]{1,80})\b.{0,80}?\bnew album\b.{0,40}?["\u201c](?P<album>[^"\n\u201d]{2,120})["\u201d]',
        r'(?is)["\u201c](?P<album>[^"\n\u201d]{2,120})["\u201d].{0,80}?\bby\b\s+(?P<artist>[A-Z0-9][A-Za-z0-9 &+!\'\-.]{1,80})',
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            artist = clean_capture(match.group("artist"))
            album = clean_capture(match.group("album"))
            if artist and album:
                return artist, album

    subject_match = re.search(r"(?im)^subject:\s*(.+)$", text)
    if subject_match:
        subject = subject_match.group(1).strip()
        subject_patterns = [
            r'(?i)(?P<artist>.+?)\s*[-–:]\s*["\u201c]?(?P<album>.+?)["\u201d]?\s*(?:out now|new album|album release|released)?$',
            r'(?i)new album from\s+(?P<artist>.+?)\s*[-–:]\s*["\u201c]?(?P<album>.+?)["\u201d]?$',
        ]
        for pattern in subject_patterns:
            match = re.search(pattern, subject)
            if match:
                artist = clean_capture(match.group("artist"))
                album = clean_capture(match.group("album"))
                if artist and album:
                    return artist, album

    return None, None


def artist_names_from_result(result: dict) -> str:
    artists = result.get("artists")
    if isinstance(artists, list) and artists:
        names = [a.get("name", "") for a in artists if a.get("name")]
        if names:
            return ", ".join(names)
    artist = result.get("artist")
    if isinstance(artist, str):
        return artist
    return ""


def score_album_result(result: dict, target_artist: str, target_album: str) -> int:
    result_artist = normalize(artist_names_from_result(result))
    result_album = normalize(result.get("title", ""))
    result_type = str(result.get("type", "")).lower()
    playlist_id = result.get("playlistId")

    if not playlist_id:
        return -999

    score = 0
    if result_type == "album":
        score += 2
    if result_album == target_album:
        score += 5
    elif target_album in result_album or result_album in target_album:
        score += 2
    if result_artist == target_artist:
        score += 4
    elif target_artist in result_artist or result_artist in target_artist:
        score += 2

    return score


def best_album_match(ytmusic: YTMusic, artist: str, album: str) -> Optional[dict]:
    query = f"{artist} {album}"
    results = ytmusic.search(query, filter="albums", limit=10)

    target_artist = normalize(artist)
    target_album = normalize(album)

    scored = [(score_album_result(r, target_artist, target_album), r) for r in results]
    scored.sort(key=lambda x: x[0], reverse=True)

    if not scored:
        return None

    best_score, best_result = scored[0]
    log(f"Top match score: {best_score} | {artist_names_from_result(best_result)} - {best_result.get('title')}")

    if best_score >= MIN_MATCH_SCORE:
        return best_result

    return None


def connect_gmail():
    ssl_context = ssl.create_default_context()
    mail = imaplib.IMAP4_SSL(GMAIL_HOST, ssl_context=ssl_context)
    mail.login(GMAIL_USER, GMAIL_APP_PASSWORD)
    mail.select('"[Gmail]/All Mail"')
    return mail


def search_target_emails(mail):
    typ, data = mail.uid("SEARCH", "X-GM-RAW", f'"{GMAIL_QUERY}"')
    if typ != "OK":
        raise RuntimeError("Failed to search Gmail with X-GM-RAW.")
    if not data or not data[0]:
        return []
    return data[0].split()


def fetch_message(mail, uid: bytes):
    typ, msg_data = mail.uid("FETCH", uid, "(RFC822)")
    if typ != "OK" or not msg_data or not msg_data[0]:
        return None
    return email.message_from_bytes(msg_data[0][1])


def mark_seen(mail, uid: bytes) -> None:
    mail.uid("STORE", uid, "+FLAGS", r"(\Seen)")


def main() -> None:
    ytmusic = YTMusic(
        YTMUSIC_AUTH_FILE,
        oauth_credentials=OAuthCredentials(
            client_id=YT_CLIENT_ID,
            client_secret=YT_CLIENT_SECRET,
        ),
    )

    mail = connect_gmail()
    try:
        uids = search_target_emails(mail)
        log(f"Found {len(uids)} unread labeled email(s).")

        for uid in uids:
            msg = fetch_message(mail, uid)
            if msg is None:
                log("Skipping email: could not fetch message.")
                continue

            subject = decode_subject(msg.get("Subject", ""))
            text = extract_email_text(msg)

            log("")
            log("=" * 80)
            log(f"Subject: {subject}")

            artist, album = extract_artist_album(text)
            if not artist or not album:
                log("Could not parse artist/album. Leaving unread.")
                continue

            log(f"Parsed artist: {artist}")
            log(f"Parsed album:  {album}")

            match = best_album_match(ytmusic, artist, album)
            if not match:
                log("No confident YouTube Music match found. Leaving unread.")
                continue

            playlist_id = match["playlistId"]
            log(f"Matched album: {artist_names_from_result(match)} - {match.get('title')}")
            log(f"playlistId: {playlist_id}")

            response = ytmusic.rate_playlist(playlist_id, "LIKE")
            log(f"Added album to library. API response: {response}")

            mark_seen(mail, uid)
            log("Marked email as read.")

    finally:
        mail.logout()


if __name__ == "__main__":
    main()