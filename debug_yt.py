import os
import json
import time
import requests

# Force refresh token
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
new_token = refresh.json()
access_token = new_token["access_token"]
print(f"Fresh token: {access_token[:30]}...")

# Test directly with fresh token
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "Origin": "https://music.youtube.com",
    "Referer": "https://music.youtube.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

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
    "query": "Adele Hello"
}

url = "https://music.youtube.com/youtubei/v1/search?alt=json&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30"
response = requests.post(url, headers=headers, json=body)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:1000]}")