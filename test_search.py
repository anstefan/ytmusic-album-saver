import json
import logging
from ytmusicapi import YTMusic

logging.basicConfig(level=logging.DEBUG)

with open("oauth.json") as f:
    parsed = json.load(f)
    print(f"oauth.json keys: {list(parsed.keys())}")

yt = YTMusic("oauth.json")
results = yt.search("Kanye West Vultures", filter="albums", limit=3)
print(results)