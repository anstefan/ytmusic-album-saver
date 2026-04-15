import os
import json
import time
import requests

# Refresh token
with open("oauth.json") as f:
    oauth = json.load(f)

refresh = requests.post(
    "https://oauth2.googleapis.com/token",
    data={
        "client_id": os.environ["YT_CLIENT_ID"],
        "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": oauth["refresh_token"],
        "grant_type": "refresh_token",
    }
)
token = refresh.json()["access_token"]
print(f"Fresh token: {token[:30]}...")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Origin": "https://music.youtube.com",
    "Referer": "https://music.youtube.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Goog-AuthUser": "0",
}

# rate_playlist body - LIKE = add to library
body = {
    "context": {
        "client": {
            "clientName": "WEB_REMIX",
            "clientVersion": "1.20220918.01.00",
            "hl": "en",
            "gl": "US",
        },
        "user": {}
    },
    "target": {
        "playlistId": "OLAK5uy_l6pEkEJgy577R-ySAoobVoHRCok9VNDCY"
    },
    "rating": "LIKE"
}

url = "https://music.youtube.com/youtubei/v1/like/playlist?alt=json&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30"
response = requests.post(url, headers=headers, json=body)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:2000]}")