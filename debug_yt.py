import os
import json
import requests
from ytmusicapi import YTMusic, OAuthCredentials
from ytmusicapi.constants import YTM_BASE_API, YTM_PARAMS, YTM_PARAMS_KEY

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

# Make the raw request manually to see full error
token = yt.auth.access_token
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "X-Goog-AuthUser": "0",
    "x-origin": "https://music.youtube.com",
}

body = {"context": yt.context["context"], "query": "Adele Hello"}
url = f"{YTM_BASE_API}search?{YTM_PARAMS}&key={YTM_PARAMS_KEY}"
print(f"URL: {url}")

response = requests.post(url, headers=headers, json=body)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:2000]}")