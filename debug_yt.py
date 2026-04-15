import os
from ytmusicapi import YTMusic, OAuthCredentials

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