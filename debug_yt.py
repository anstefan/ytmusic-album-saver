import os
from ytmusicapi import YTMusic, OAuthCredentials

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

# Hardcode a known visitor_data value
yt.context["client"]["visitorData"] = "CgtDSkFYeG8yY0FUNCiDt7e2BjIKCgJVUxIEGgAgYQ%3D%3D"
print(f"visitor_data set: {yt.context['client']['visitorData']}")

results = yt.search("Adele Hello", filter="albums", limit=3)
print(f"Found {len(results)} results")
print(results[0] if results else "No results")