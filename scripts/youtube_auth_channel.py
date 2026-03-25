#!/usr/bin/env python3
"""Authorize a specific YouTube brand channel and save its token."""
import os, json, sys
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube"]
SECRET = os.path.join(os.path.dirname(__file__), "youtube_client_secret.json")

channel = sys.argv[1] if len(sys.argv) > 1 else "unknown"
TOKEN = os.path.join(os.path.dirname(__file__), f"youtube_token_{channel}.json")

print(f"\n{'='*60}")
print(f"Authorizing channel: {channel.upper()}")
print(f"⚠️  In the browser — select the '{channel.upper()}' channel, NOT your main account")
print(f"{'='*60}\n")

flow = InstalledAppFlow.from_client_secrets_file(SECRET, SCOPES)
creds = flow.run_local_server(port=8770, open_browser=True)

with open(TOKEN, "w") as f:
    f.write(creds.to_json())

yt = build("youtube", "v3", credentials=creds)
resp = yt.channels().list(part="snippet", mine=True).execute()
items = resp.get("items", [])
if items:
    name = items[0]["snippet"]["title"]
    cid  = items[0]["id"]
    print(f"\n✅ Token saved for: {name} ({cid})")
    print(f"   File: {TOKEN}")
else:
    print("⚠️  No channel found — wrong account selected?")
