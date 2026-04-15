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

print(f"headers: {yt.headers}")

body = {"context": yt.context["context"], "query": "Adele Hello"}
url = f"{YTM_BASE_API}search?{YTM_PARAMS}&key={YTM_PARAMS_KEY}"
print(f"URL: {url}")

response = requests.post(url, headers=yt.headers, json=body)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:3000]}")