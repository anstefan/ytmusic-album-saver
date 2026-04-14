import os
import json
from ytmusicapi import YTMusic, OAuthCredentials

# Debug: print oauth.json contents
with open("oauth.json") as f:
    contents = f.read()
    print(f"oauth.json length: {len(contents)}")
    try:
        parsed = json.loads(contents)
        print(f"oauth.json keys: {list(parsed.keys())}")
    except Exception as e:
        print(f"oauth.json is NOT valid JSON: {e}")
        print(f"First 200 chars: {contents[:200]}")

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

results = yt.search("Kanye West Vultures", filter="albums", limit=3)
print(results)