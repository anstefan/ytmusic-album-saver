import os
import json
from ytmusicapi import YTMusic, OAuthCredentials

# Check token before
with open("oauth.json") as f:
    before = json.load(f)
print(f"Token before: {before['access_token'][:30]}...")
print(f"expires_at before: {before['expires_at']}")

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

# Check what token ytmusicapi is actually using in headers
print(f"Auth header: {yt.headers.get('authorization', 'NOT SET')[:30]}...")

results = yt.search("Adele Hello", filter="albums", limit=3)
print(f"Found {len(results)} results")