import os
import json
from ytmusicapi import YTMusic, OAuthCredentials

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

# Print the context being used
print(f"visitor_data: {yt.context.get('client', {}).get('visitorData', 'NOT SET')}")

results = yt.search("Adele Hello", filter="albums", limit=3)
print(results)