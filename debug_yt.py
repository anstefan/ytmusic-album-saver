import os
from ytmusicapi import YTMusic, OAuthCredentials

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

print(f"context keys: {list(yt.context.keys())}")
print(f"full context: {yt.context}")