import os
import json
import time
import requests
from ytmusicapi import YTMusic, OAuthCredentials

# Force refresh token manually
with open("oauth.json") as f:
    oauth = json.load(f)

print(f"Token expired: {oauth['expires_at'] < time.time()}")

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
print(f"New token prefix: {new_token['access_token'][:30]}...")

# Update oauth.json with fresh token
oauth["access_token"] = new_token["access_token"]
oauth["expires_at"] = int(time.time()) + new_token["expires_in"]

with open("oauth.json", "w") as f:
    json.dump(oauth, f)

print("oauth.json updated with fresh token")

# Now initialize ytmusicapi
yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

results = yt.search("Adele Hello", filter="albums", limit=3)
print(f"Found {len(results)} results")
print(results[0] if results else "No results")