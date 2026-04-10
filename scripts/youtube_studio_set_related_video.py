#!/usr/bin/env python3
"""Set YouTube Shorts related videos through YouTube Studio.

This uses a signed-in Chrome profile plus AppleScript/DOM automation because the
public YouTube Data API does not expose the Shorts related-video picker.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


CHROME_APP = "/Applications/Google Chrome.app"
LOCAL_STATE = Path.home() / "Library/Application Support/Google/Chrome/Local State"
DEFAULT_MANAGER_EMAIL = "tobyglenn@gmail.com"


def run(
    cmd: list[str], *, check: bool = True, timeout: float = 20.0
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        check=check,
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def run_applescript(script: str) -> str:
    result = run(["osascript", "-e", script])
    return result.stdout.strip()


def chrome_exec_js(js: str) -> str:
    script = (
        'tell application "Google Chrome"\n'
        "set t to active tab of front window\n"
        f"return execute t javascript {json.dumps(js)}\n"
        "end tell"
    )
    return run_applescript(script)


def chrome_navigate(url: str) -> None:
    script = (
        'tell application "Google Chrome"\n'
        "activate\n"
        "if (count of windows) is 0 then error \"No Chrome windows\"\n"
        "set URL of active tab of front window to "
        f"{json.dumps(url)}\n"
        "end tell"
    )
    run_applescript(script)


def chrome_reload() -> None:
    script = (
        'tell application "Google Chrome"\n'
        "reload active tab of front window\n"
        "end tell"
    )
    run_applescript(script)


def resolve_profile(manager_email: str) -> str:
    if not LOCAL_STATE.exists():
        raise RuntimeError(f"Chrome Local State not found: {LOCAL_STATE}")
    data = json.loads(LOCAL_STATE.read_text())
    cache = data.get("profile", {}).get("info_cache", {})
    email = manager_email.lower()
    for directory, info in cache.items():
        if info.get("user_name", "").lower() == email:
            return directory
    raise RuntimeError(f"Could not resolve Chrome profile for {manager_email}")


def launch_chrome(profile_directory: str, url: str) -> None:
    run(["pkill", "-f", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"], check=False)
    time.sleep(1.0)
    run(
        [
            "open",
            "-na",
            CHROME_APP,
            "--args",
            f"--profile-directory={profile_directory}",
            "--new-window",
            url,
        ]
    )


def wait_for(js: str, *, timeout_s: float = 20.0, interval_s: float = 0.5) -> str:
    deadline = time.time() + timeout_s
    last = ""
    while time.time() < deadline:
        last = chrome_exec_js(js)
        if last and last not in {"false", "null", "undefined", "MISSING"}:
            return last
        time.sleep(interval_s)
    raise TimeoutError(f"Timed out waiting for page condition. Last result: {last!r}")


def ensure_page_ready(video_id: str) -> None:
    wait_for(
        """(() => {
            const body = document.body ? document.body.innerText : '';
            if (body.includes("Oops, you don't have permission")) return 'NO_ACCESS';
            const ok = document.querySelector('#linked-video-editor-link');
            return ok ? 'READY' : '';
        })()"""
    )
    access_state = chrome_exec_js(
        """(() => {
            const body = document.body ? document.body.innerText : '';
            return body.includes("Oops, you don't have permission") ? 'NO_ACCESS' : 'OK';
        })()"""
    )
    if access_state == "NO_ACCESS":
        raise RuntimeError(f"Authenticated profile does not have Studio access for {video_id}")


def open_related_video_picker() -> None:
    result = chrome_exec_js(
        """(() => {
            const root = document.querySelector('#linked-video-editor-link');
            if (!root) return 'NO_TRIGGER';
            const target = root.querySelector('[role=button]') || root;
            target.scrollIntoView({block: 'center'});
            target.focus();
            for (const type of ['pointerdown', 'mousedown', 'mouseup', 'click']) {
              target.dispatchEvent(new MouseEvent(type, {
                bubbles: true,
                cancelable: true,
                view: window,
                button: 0,
                buttons: 1,
              }));
            }
            target.dispatchEvent(new KeyboardEvent('keydown', {
              key: 'Enter',
              code: 'Enter',
              keyCode: 13,
              which: 13,
              bubbles: true,
            }));
            target.dispatchEvent(new KeyboardEvent('keyup', {
              key: 'Enter',
              code: 'Enter',
              keyCode: 13,
              which: 13,
              bubbles: true,
            }));
            return 'CLICKED';
        })()"""
    )
    if result != "CLICKED":
        raise RuntimeError(f"Failed to open related video picker: {result}")
    wait_for(
        """(() => document.querySelector('ytcp-video-pick-dialog') ? 'OPEN' : '')()""",
        timeout_s=10.0,
    )


def inject_related_video(related_video_id: str, related_title: str) -> None:
    payload = {"videoId": related_video_id, "sectionTitle": "", "title": related_title}
    result = chrome_exec_js(
        f"""(() => {{
            const dlg = document.querySelector('ytcp-video-pick-dialog');
            const picker = document.querySelector('ytcp-shorts-content-links-picker');
            if (!picker) return 'NO_PICKER';
            const ev = new CustomEvent('video-picked', {{
              bubbles: true,
              composed: true,
              detail: {json.dumps(payload)},
            }});
            if (dlg) dlg.dispatchEvent(ev);
            picker.dispatchEvent(ev);
            const close = document.querySelector('ytcp-video-pick-dialog #close');
            if (close) close.click();
            return document.querySelector('#linked-video-editor-link .dropdown-trigger-text')?.innerText?.trim() || '';
        }})()"""
    )
    if result != related_title:
        raise RuntimeError(
            f"Picker label did not update to expected title. expected={related_title!r} actual={result!r}"
        )


def save_changes() -> None:
    chrome_exec_js(
        """(() => {
            const save = [...document.querySelectorAll('*')].find(
              el => (el.innerText || '').trim() === 'Save'
            );
            if (!save) return 'NO_SAVE';
            save.click();
            return 'CLICKED';
        })()"""
    )
    wait_for(
        """(() => {
            const save = [...document.querySelectorAll('*')].find(
              el => (el.innerText || '').trim() === 'Save'
            );
            const body = document.body ? document.body.innerText : '';
            const disabled = save ? (save.getAttribute('aria-disabled') || String(save.hasAttribute('disabled'))) : '';
            return body.includes('All changes saved.') && (disabled === 'true' || disabled === 'True')
              ? 'SAVED'
              : '';
        })()""",
        timeout_s=20.0,
    )


def verify_related_title(expected_title: str) -> None:
    chrome_reload()
    time.sleep(8.0)
    wait_for(
        """(() => {
            const body = document.body ? document.body.innerText : '';
            return body.includes('Video details') && document.querySelector('#linked-video-editor-link') ? 'READY' : '';
        })()""",
        timeout_s=20.0,
    )
    label = chrome_exec_js(
        """(() => document.querySelector('#linked-video-editor-link .dropdown-trigger-text')?.innerText?.trim() || '')()"""
    )
    if label != expected_title:
        raise RuntimeError(
            f"Reload verification failed. expected related title {expected_title!r}, got {label!r}"
        )


def set_related_video(short_video_id: str, related_video_id: str, related_title: str) -> None:
    print(f"{short_video_id}: opening Studio edit page", flush=True)
    chrome_navigate(f"https://studio.youtube.com/video/{short_video_id}/edit")
    time.sleep(8.0)
    ensure_page_ready(short_video_id)
    current = chrome_exec_js(
        """(() => document.querySelector('#linked-video-editor-link .dropdown-trigger-text')?.innerText?.trim() || '')()"""
    )
    if current == related_title:
        verify_related_title(related_title)
        print(f"{short_video_id}: already set -> {related_title}", flush=True)
        return
    print(f"{short_video_id}: opening related-video picker", flush=True)
    open_related_video_picker()
    print(f"{short_video_id}: injecting related video {related_video_id}", flush=True)
    inject_related_video(related_video_id, related_title)
    print(f"{short_video_id}: saving changes", flush=True)
    save_changes()
    verify_related_title(related_title)
    print(
        f"{short_video_id}: set related video -> {related_video_id} ({related_title})",
        flush=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manager-email", default=DEFAULT_MANAGER_EMAIL)
    parser.add_argument("--profile-directory")
    parser.add_argument("--pair", action="append", default=[], help="short_id:related_id:related_title")
    args = parser.parse_args()

    if not args.pair:
        parser.error("at least one --pair is required")

    profile_directory = args.profile_directory or resolve_profile(args.manager_email)

    first_short = args.pair[0].split(":", 2)[0]
    launch_chrome(profile_directory, f"https://studio.youtube.com/video/{first_short}/edit")
    time.sleep(8.0)
    wait_for("""(() => document.body ? 'BODY' : '')()""", timeout_s=15.0)

    for raw_pair in args.pair:
        short_id, related_id, related_title = raw_pair.split(":", 2)
        set_related_video(short_id, related_id, related_title)

    return 0


if __name__ == "__main__":
    sys.exit(main())
