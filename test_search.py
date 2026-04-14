import os
import json
import logging
from ytmusicapi import YTMusic, OAuthCredentials

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Print oauth.json contents
with open("oauth.json") as f:
    parsed = json.load(f)
    print(f"oauth.json keys: {list(parsed.keys())}")
    print(f"token_type: {parsed.get('token_type')}")
    print(f"scope: {parsed.get('scope')}")
    print(f"expires_at: {parsed.get('expires_at')}")

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

results = yt.search("Kanye West Vultures", filter="albums", limit=3)
print(results)