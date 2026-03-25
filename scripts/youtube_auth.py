#!/usr/bin/env python3
"""Run OAuth flow and list all YouTube channels accessible to the account."""
import os, json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube"]
SECRET = os.path.join(os.path.dirname(__file__), "youtube_client_secret.json")
TOKEN  = os.path.join(os.path.dirname(__file__), "youtube_token.json")

flow = InstalledAppFlow.from_client_secrets_file(SECRET, SCOPES)
creds = flow.run_local_server(port=8766, open_browser=True)

with open(TOKEN, "w") as f:
    f.write(creds.to_json())
print("✅ Token saved to", TOKEN)

yt = build("youtube", "v3", credentials=creds)
resp = yt.channels().list(part="snippet", mine=True).execute()
print("\nChannels accessible:")
for ch in resp.get("items", []):
    print(f"  {ch['snippet']['title']} — {ch['id']}")
