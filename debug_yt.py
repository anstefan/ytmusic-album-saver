import os
import json
import requests

# Read oauth.json
with open("oauth.json") as f:
    oauth = json.load(f)

print(f"Current access_token prefix: {oauth['access_token'][:20]}...")
print(f"expires_at: {oauth['expires_at']}")

# Force refresh the token
client_id = os.environ["YT_CLIENT_ID"]
client_secret = os.environ["YT_CLIENT_SECRET"]

refresh_response = requests.post(
    "https://oauth2.googleapis.com/token",
    data={
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": oauth["refresh_token"],
        "grant_type": "refresh_token",
    }
)

print(f"Refresh status: {refresh_response.status_code}")
print(f"Refresh response: {refresh_response.text}")