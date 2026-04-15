import os
import json
import time
import requests
from ytmusicapi import YTMusic, OAuthCredentials

# Step 1: Search without auth
search_headers = {
    "Content-Type": "application/json",
    "Origin": "https://music.youtube.com",
    "Referer": "https://music.youtube.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}

search_body = {
    "context": {
        "client": {
            "clientName": "WEB_REMIX",
            "clientVersion": "1.20220918.01.00",
            "hl": "en",
            "gl": "US",
        },
        "user": {}
    },
    "query": "Adele Hello",
    "params": "EgWKAQIYAWoKEAoQAxAEEAkQBQ%3D%3D"
}

url = "https://music.youtube.com/youtubei/v1/search?alt=json&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30"
response = requests.post(url, headers=search_headers, json=search_body)
print(f"Search status: {response.status_code}")

# Step 2: Use OAuth for rate_playlist
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
oauth["access_token"] = new_token["access_token"]
oauth["expires_at"] = int(time.time()) + new_token["expires_in"]

with open("oauth.json", "w") as f:
    json.dump(oauth, f)

print("Token refreshed, initializing YTMusic for library action...")

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

# Test rate_playlist with a known playlist ID (Adele - 30)
result = yt.rate_playlist("OLAK5uy_l6pEkEJgy577R-ySAoobVoHRCok9VNDCY", "LIKE")
print(f"rate_playlist result: {result}")