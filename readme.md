# ytmusic-album-saver

Automatically saves new album releases to your YouTube Music library.

Monitors a Gmail label for release notification emails (e.g. from [muspy.com](https://muspy.com)), parses the artist and album name, searches YouTube Music, and saves matching albums to your library. Runs hourly via GitHub Actions.

---

## How it works

1. muspy.com sends an email when a followed artist releases new music
2. Gmail filters those emails into the `album-release` label
3. GitHub Actions runs the sync script every hour
4. The script reads unread labeled emails and parses artist + album
5. It searches YouTube Music for the best match
6. On a confident match, it saves the album to your YouTube Music library
7. The email is marked as read so it won't be processed again

---

## Prerequisites

- A [muspy.com](https://muspy.com) account with artists you follow
- A Gmail account that receives muspy release notifications
- A GitHub account
- Python 3.11+ (for local setup steps only)

---

## Setup

### 1. Gmail label and filter

In Gmail, create a label called `album-release`.

Then create a filter that applies this label to muspy notification emails:
- **From:** `info@muspy.com`
- **Action:** Apply label `album-release`, skip inbox (optional)

### 2. Gmail IMAP and App Password

1. In Gmail → **Settings → See all settings → Forwarding and POP/IMAP** → enable IMAP
2. Go to [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3. Create an App Password (requires 2-Step Verification)
4. Save the 16-character password

### 3. YouTube Music browser auth

The script authenticates with YouTube Music using your browser session cookies. This needs to be refreshed periodically (every few weeks).

**To generate `browser.json`:**

Install ytmusicapi locally:
```bash
pip install ytmusicapi
```

Run the browser setup:
```bash
ytmusicapi browser
```

When prompted, paste your request headers from Chrome DevTools:
1. Open [music.youtube.com](https://music.youtube.com) in Chrome while logged in
2. Press **F12** → **Network** tab
3. Click any request to `music.youtube.com/youtubei/v1/`
4. Right-click → **Copy → Copy as cURL (bash)**
5. Extract and paste the headers when prompted

Then base64-encode the file for GitHub:

**Mac/Linux:**
```bash
base64 -i browser.json | tr -d '\n' | pbcopy
```

**Windows (PowerShell):**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("browser.json")) | Set-Clipboard
```

### 4. GitHub repository

Create a new **private** GitHub repository and push these files: