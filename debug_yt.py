import os
import json
import requests
from ytmusicapi import YTMusic, OAuthCredentials

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

# Override with known working client version
body = {
    "context": {
        "client": {
            "clientName": "WEB_REMIX",
            "clientVersion": "1.20220918.01.00",
            "hl": "en",
            "gl": "US",
            "visitorData": yt.headers.get("X-Goog-Visitor-Id", ""),
        },
        "user": {}
    },
    "query": "Adele Hello"
}

url = "https://music.youtube.com/youtubei/v1/search?alt=json&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30"

print(f"Request body: {json.dumps(body, indent=2)}")

response = requests.post(url, headers=yt.headers, json=body)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:3000]}")