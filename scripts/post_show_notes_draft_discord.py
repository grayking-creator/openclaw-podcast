#!/usr/bin/env python3
"""Post an AgentStack Daily research draft to its Discord episode channel.

The show-notes draft is uploaded as a Markdown attachment instead of pasted as
many Discord messages. That keeps formatting intact and avoids retry duplicates
when Discord rate-limits long posts.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPTS_DIR.parent
ENV_FILE = Path.home() / ".openclaw/.env"
OPENCLAW_CONFIG = Path.home() / ".openclaw/openclaw.json"
GUILD_ID = "1475905694145318944"


def load_env_key(name: str) -> str:
    if not ENV_FILE.exists():
        return ""
    for line in ENV_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith(f"{name}="):
            return line.split("=", 1)[1].strip().strip("\"'")
    return ""


def load_discord_bot_token() -> str:
    if OPENCLAW_CONFIG.exists():
        try:
            config = json.loads(OPENCLAW_CONFIG.read_text(encoding="utf-8", errors="ignore"))
            token = config["channels"]["discord"]["accounts"]["default"].get("token", "")
            if token:
                return str(token).strip().strip("\"'")
        except Exception:
            pass
    return load_env_key("DISCORD_BOT_TOKEN")


def request_json(method: str, url: str, token: str, payload: dict | None = None) -> dict | list:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (https://github.com/openclaw/openclaw, 1.0)",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        raw = resp.read()
        return json.loads(raw) if raw else {}


def discord_request(method: str, path: str, token: str, payload: dict | None = None) -> dict | list:
    return request_json(method, f"https://discord.com/api/v10{path}", token, payload)


def ensure_channel(ep_num: int, title: str, token: str) -> dict:
    name = f"agent-stack-ep{ep_num:03d}"
    channels = discord_request("GET", f"/guilds/{GUILD_ID}/channels", token)
    for channel in channels:
        if channel.get("name") == name:
            return channel
    return discord_request(
        "POST",
        f"/guilds/{GUILD_ID}/channels",
        token,
        {
            "name": name,
            "type": 0,
            "topic": f"AgentStack Daily EP {ep_num:03d} - {title} | Research Draft",
        },
    )


def extract_title(notes: str, ep_num: int) -> str:
    for line in notes.splitlines():
        if line.startswith("# "):
            return line.strip("# ").strip()
    return f"EP{ep_num:03d} Research Draft"


def extract_section(notes: str, heading: str) -> str:
    lines: list[str] = []
    capture = False
    for raw in notes.splitlines():
        line = raw.rstrip()
        if line.strip() == f"## {heading}":
            capture = True
            continue
        if capture and line.startswith("## "):
            break
        if capture:
            lines.append(line)
    return "\n".join(lines).strip()


def extract_topic_summary(notes: str, max_items: int = 10) -> str:
    """Return a short topic summary for Discord review posts."""
    lines = []
    in_slate = False
    for raw in notes.splitlines():
        line = raw.strip()
        if line == "## Story Slate":
            in_slate = True
            continue
        if in_slate and line.startswith("## "):
            break
        if not in_slate:
            continue
        numbered = re.match(r"^\d+\.\s+\*\*(.+?)\*\*", line)
        if numbered:
            lines.append(numbered.group(1).strip())
        if line.startswith("### "):
            title = line.lstrip("#").strip()
            title = title.split("**", 2)[1] if "**" in title else title
            title = title.strip(" *")
            if title:
                lines.append(title)
        if len(lines) >= max_items:
            break

    if not lines:
        return "Topics:\n- See attached show notes."

    return "Topics:\n" + "\n".join(f"{idx}. {item}" for idx, item in enumerate(lines[:max_items], 1))


def multipart_body(payload: dict, file_path: Path) -> tuple[bytes, str]:
    boundary = f"----openclaw-{uuid.uuid4().hex}"
    mime = mimetypes.guess_type(str(file_path))[0] or "text/markdown"
    file_bytes = file_path.read_bytes()
    parts = [
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="payload_json"\r\n'
        "Content-Type: application/json\r\n\r\n"
        f"{json.dumps(payload)}\r\n".encode("utf-8"),
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="files[0]"; filename="{file_path.name}"\r\n'
        f"Content-Type: {mime}\r\n\r\n".encode("utf-8"),
        file_bytes,
        f"\r\n--{boundary}--\r\n".encode("utf-8"),
    ]
    return b"".join(parts), boundary


def post_attachment(channel_id: str, token: str, file_path: Path, content: str) -> dict:
    payload = {
        "content": content,
        "attachments": [{"id": "0", "filename": file_path.name}],
    }
    body, boundary = multipart_body(payload, file_path)
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    for _ in range(8):
        req = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Authorization": f"Bot {token}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "User-Agent": "DiscordBot (https://github.com/openclaw/openclaw, 1.0)",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            if exc.code != 429:
                raise
            try:
                wait = float(json.loads(exc.read().decode("utf-8") or "{}").get("retry_after", 2))
            except Exception:
                wait = 2.0
            time.sleep(wait + 0.5)
    raise RuntimeError("Discord upload failed after rate-limit retries")


def edit_message(channel_id: str, message_id: str, token: str, content: str) -> None:
    discord_request("PATCH", f"/channels/{channel_id}/messages/{message_id}", token, {"content": content})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode", type=int)
    parser.add_argument("--file", type=Path)
    parser.add_argument("--channel-id", help="Post to an existing Discord channel id instead of looking up/creating by name")
    parser.add_argument("--note", default="",
                        help="Status line appended after the topic summary (e.g. the "
                             "'transcript generation in progress — reject now' mid-stream notice)")
    parser.add_argument("--headline", default="",
                        help="Override the leading headline line (default: 'show notes are ready')")
    args = parser.parse_args()

    ep_str = f"{args.episode:03d}"
    draft_path = args.file or PODCAST_DIR / f"show_notes_episode_{ep_str}.md"
    if not draft_path.exists():
        raise SystemExit(f"Missing draft file: {draft_path}")
    token = load_discord_bot_token()
    if not token:
        raise SystemExit("DISCORD_BOT_TOKEN is not configured")

    notes = draft_path.read_text(encoding="utf-8", errors="ignore")
    title = extract_title(notes, args.episode)
    if args.channel_id:
        channel = {"id": args.channel_id, "name": f"channel:{args.channel_id}"}
    else:
        channel = ensure_channel(args.episode, title, token)
    summary = extract_topic_summary(notes)
    headline = args.headline.strip() or f"AgentStack Daily EP{ep_str} show notes are ready."
    note_block = f"\n{args.note.strip()}\n" if args.note.strip() else ""
    content = (
        f"{headline}\n\n"
        f"{summary}\n"
        f"{note_block}"
        "\nShow notes: uploading attachment..."
    )
    message = post_attachment(str(channel["id"]), token, draft_path, content)
    attachment_url = ""
    attachments = message.get("attachments") if isinstance(message, dict) else None
    if attachments:
        attachment_url = attachments[0].get("url", "")
    if attachment_url and message.get("id"):
        edit_message(
            str(channel["id"]),
            str(message["id"]),
            token,
            f"{headline}\n\n{summary}\n{note_block}\nShow notes: {attachment_url}",
        )
    print(f"Posted {draft_path.name} to #{channel['name']} ({channel['id']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
