import os
import json
import requests

# Read token directly from oauth.json
with open("oauth.json") as f:
    oauth = json.load(f)

token = oauth["access_token"]
print(f"Token prefix: {token[:20]}...")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Origin": "https://music.youtube.com",
    "Referer": "https://music.youtube.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "X-Youtube-Client-Name": "67",
    "X-Youtube-Client-Version": "1.20220918.01.00",
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
print(f"Response: {response.text[:3000]}")