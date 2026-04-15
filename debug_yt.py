import os
import requests
from ytmusicapi import YTMusic, OAuthCredentials

# Fetch visitor_data from YouTube Music first
response = requests.get("https://music.youtube.com")
visitor_data = None
for line in response.text.split("\n"):
    if "visitorData" in line:
        import re
        match = re.search(r'"visitorData"\s*:\s*"([^"]+)"', line)
        if match:
            visitor_data = match.group(1)
            break

print(f"Fetched visitor_data: {visitor_data}")

yt = YTMusic(
    "oauth.json",
    oauth_credentials=OAuthCredentials(
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
    ),
)

if visitor_data:
    yt.context["client"]["visitorData"] = visitor_data

print(f"visitor_data set: {yt.context.get('client', {}).get('visitorData', 'NOT SET')}")

results = yt.search("Adele Hello", filter="albums", limit=3)
print(f"Found {len(results)} results")
print(results[0] if results else "No results")