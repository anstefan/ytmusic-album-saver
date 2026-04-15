import os
import json
import time
import requests
import unittest.mock as mock
from ytmusicapi import YTMusic, OAuthCredentials

# Refresh token first
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
oauth["access_token"] = refresh.json()["access_token"]
oauth["expires_at"] = int(time.time()) + 3599
with open("oauth.json", "w") as f:
    json.dump(oauth, f)

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

# Intercept _send_request to see what it's sending
original_send = yt._send_request
def debug_send(endpoint, body):
    print(f"Endpoint: {endpoint}")
    print(f"Body: {json.dumps(body, indent=2)}")
    return original_send(endpoint, body)

yt._send_request = debug_send

try:
    yt.rate_playlist("OLAK5uy_l6pEkEJgy577R-ySAoobVoHRCok9VNDCY", "LIKE")
except Exception as e:
    print(f"Error: {e}")