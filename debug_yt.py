import os
from ytmusicapi import YTMusic, OAuthCredentials
from ytmusicapi.constants import VISITOR_DATA

print(f"Default visitor_data: {VISITOR_DATA}")

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

yt.context["client"]["visitorData"] = VISITOR_DATA
print(f"visitor_data set: {yt.context['client']['visitorData']}")

results = yt.search("Adele Hello", filter="albums", limit=3)
print(f"Found {len(results)} results")