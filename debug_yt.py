import os
import requests
from ytmusicapi import YTMusic, OAuthCredentials

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

body = {"context": yt.context["context"], "query": "Adele Hello"}
url = "https://music.youtube.com/youtubei/v1/search?alt=json&key=AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30"
print(f"URL: {url}")

response = requests.post(url, headers=yt.headers, json=body)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:3000]}")