#!/usr/bin/env python3
"""Set YouTube Shorts related videos through YouTube Studio.

This uses a signed-in Chrome profile plus AppleScript/DOM automation because the
public YouTube Data API does not expose the Shorts related-video picker.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path


CHROME_APP = "/Applications/Google Chrome.app"
LOCAL_STATE = Path.home() / "Library/Application Support/Google/Chrome/Local State"
DEFAULT_MANAGER_EMAIL = os.environ.get("YOUTUBE_STUDIO_MANAGER_EMAIL") or "tobypeters@gmail.com"
DEFAULT_PROFILE_DIRECTORY = os.environ.get("YOUTUBE_STUDIO_PROFILE_DIRECTORY", "")
EMAIL_ALIASES = {
    "tobyglenn@gmail.com": ["tobypeters@gmail.com"],
}


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


def activate_chrome_for_retry() -> None:
    try:
        run(
            ["osascript", "-e", 'tell application "Google Chrome" to activate'],
            check=False,
            timeout=5.0,
        )
    except Exception:
        pass


def run_applescript(script: str, *, timeout: float = 20.0, retries: int = 2) -> str:
    last_error = ""
    for attempt in range(retries + 1):
        try:
            result = run(["osascript", "-e", script], timeout=timeout)
            return result.stdout.strip()
        except subprocess.TimeoutExpired as exc:
            last_error = f"osascript timed out after {exc.timeout}s"
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or exc.stdout or str(exc)).strip()
            last_error = detail or f"osascript exited {exc.returncode}"

        if attempt < retries:
            activate_chrome_for_retry()
            time.sleep(1.5 * (attempt + 1))

    raise RuntimeError(f"AppleScript command failed after {retries + 1} attempts: {last_error}")


def chrome_exec_js(js: str, *, timeout: float = 20.0, retries: int = 2) -> str:
    script = (
        'tell application "Google Chrome"\n'
        "set t to active tab of front window\n"
        f"return execute t javascript {json.dumps(js)}\n"
        "end tell"
    )
    return run_applescript(script, timeout=timeout, retries=retries)


def chrome_navigate(url: str, *, profile_directory: str = "") -> None:
    script = (
        'tell application "Google Chrome"\n'
        "activate\n"
        "if (count of windows) is 0 then error \"No Chrome windows\"\n"
        "set URL of active tab of front window to "
        f"{json.dumps(url)}\n"
        "end tell"
    )
    try:
        run_applescript(script)
    except RuntimeError as exc:
        if not profile_directory:
            raise
        print(
            f"AppleScript navigation failed ({exc}); opening a fresh Studio window",
            file=sys.stderr,
            flush=True,
        )
        launch_chrome(profile_directory, url, relaunch=False)


def chrome_reload() -> None:
    script = (
        'tell application "Google Chrome"\n'
        "reload active tab of front window\n"
        "end tell"
    )
    run_applescript(script)


def close_studio_window(short_video_id: str) -> None:
    needle = f"studio.youtube.com/video/{short_video_id}/edit"
    script = (
        'tell application "Google Chrome"\n'
        "if (count of windows) is 0 then return \"NO_WINDOWS\"\n"
        "set closedCount to 0\n"
        "repeat with windowIndex from (count of windows) to 1 by -1\n"
        "  set w to window windowIndex\n"
        "  repeat with tabIndex from (count of tabs of w) to 1 by -1\n"
        "    try\n"
        "      set tabUrl to URL of tab tabIndex of w\n"
        f"      if tabUrl contains {json.dumps(needle)} then\n"
        "        if (count of tabs of w) is 1 then\n"
        "          close w\n"
        "          set closedCount to closedCount + 1\n"
        "          exit repeat\n"
        "        else\n"
        "          close tab tabIndex of w\n"
        "          set closedCount to closedCount + 1\n"
        "        end if\n"
        "      end if\n"
        "    end try\n"
        "  end repeat\n"
        "end repeat\n"
        "return closedCount as text\n"
        "end tell"
    )
    try:
        result = run_applescript(script, timeout=8.0, retries=1)
    except RuntimeError as exc:
        print(
            f"{short_video_id}: WARN could not close Studio window: {exc}",
            file=sys.stderr,
            flush=True,
        )
        return
    if result.isdigit() and int(result) > 0:
        noun = "window/tab" if result == "1" else "windows/tabs"
        print(f"{short_video_id}: closed {result} Studio {noun}", flush=True)
    elif not result.startswith("NO_WINDOWS"):
        print(
            f"{short_video_id}: WARN Studio window left open ({result})",
            file=sys.stderr,
            flush=True,
        )


def _profile_emails(directory: str, info: dict) -> set[str]:
    emails = {str(info.get("user_name") or "").lower()}
    prefs_path = LOCAL_STATE.parent / directory / "Preferences"
    if prefs_path.exists():
        try:
            prefs = json.loads(prefs_path.read_text())
            for account in prefs.get("account_info", []) or []:
                emails.add(str(account.get("email") or "").lower())
        except Exception:
            pass
    return {email for email in emails if email}


def resolve_profile(manager_email: str) -> str:
    if not LOCAL_STATE.exists():
        raise RuntimeError(f"Chrome Local State not found: {LOCAL_STATE}")
    data = json.loads(LOCAL_STATE.read_text())
    cache = data.get("profile", {}).get("info_cache", {})
    email = manager_email.lower()
    candidate_emails = [email, *EMAIL_ALIASES.get(email, [])]
    matches = [
        directory
        for directory, info in cache.items()
        if _profile_emails(directory, info).intersection(candidate_emails)
    ]
    if not matches:
        raise RuntimeError(
            f"Could not resolve Chrome profile for {manager_email}. "
            f"Known profile emails: {', '.join(sorted(set().union(*(_profile_emails(d, i) for d, i in cache.items()))))}"
        )

    profile_meta = data.get("profile", {})
    preferred = [
        profile_meta.get("last_used"),
        *(profile_meta.get("last_active_profiles") or []),
        *(profile_meta.get("profiles_order") or []),
    ]
    for directory in preferred:
        if directory in matches:
            return directory
    return matches[0]


def launch_chrome(profile_directory: str, url: str, *, relaunch: bool = False) -> None:
    if relaunch:
        try:
            run(
                ["osascript", "-e", 'tell application "Google Chrome" to quit'],
                check=False,
                timeout=8.0,
            )
        except Exception:
            pass
        deadline = time.time() + 12.0
        while time.time() < deadline:
            probe = run(
                ["pgrep", "-f", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"],
                check=False,
                timeout=2.0,
            )
            if probe.returncode != 0:
                break
            time.sleep(0.5)
        run(["pkill", "-f", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"], check=False)
        time.sleep(2.0)
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
    last_error = ""
    while time.time() < deadline:
        try:
            remaining = max(1.0, deadline - time.time())
            last = chrome_exec_js(js, timeout=min(8.0, remaining), retries=0)
            last_error = ""
        except RuntimeError as exc:
            last_error = str(exc)
            time.sleep(interval_s)
            continue
        if last and last not in {"false", "null", "undefined", "MISSING"}:
            return last
        time.sleep(interval_s)
    suffix = f" Last error: {last_error}" if last_error else ""
    raise TimeoutError(f"Timed out waiting for page condition. Last result: {last!r}.{suffix}")


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


def related_video_label(expected_title: str = "") -> str:
    return chrome_exec_js(
        f"""(() => {{
            const root = document.querySelector('#linked-video-editor-link');
            if (!root) return '';
            const expected = {json.dumps(expected_title)};
            const fullText = (root.innerText || '').trim();
            if (expected && fullText.includes(expected)) return expected;
            return (
              root.querySelector('.dropdown-trigger-text')?.innerText?.trim()
              || fullText
              || ''
            );
        }})()"""
    )


def close_related_video_picker() -> None:
    chrome_exec_js(
        """(() => {
            const dialog = document.querySelector('ytcp-video-pick-dialog');
            if (!dialog) return 'NO_DIALOG';
            const close = dialog.querySelector('#close');
            if (close) {
              close.click();
              return 'CLICKED';
            }
            return 'NO_CLOSE';
        })()"""
    )


def has_pending_save() -> bool:
    return chrome_exec_js(
        """(() => {
            const save = document.querySelector('#save') ||
              [...document.querySelectorAll('*')].find(
                el => (el.innerText || '').trim() === 'Save'
              );
            if (!save) return 'false';
            const aria = save.getAttribute('aria-disabled');
            return (aria === 'false' || (!save.hasAttribute('disabled') && aria !== 'true'))
              ? 'true'
              : 'false';
        })()"""
    ) == "true"


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
            return 'PICKED';
        }})()"""
    )
    if result != "PICKED":
        raise RuntimeError(f"Related-video injection failed: {result}")

    deadline = time.time() + 10.0
    actual = ""
    while time.time() < deadline:
        actual = related_video_label(related_title)
        if actual == related_title:
            close_related_video_picker()
            return
        time.sleep(0.5)
    close_related_video_picker()
    if actual != related_title:
        raise RuntimeError(
            f"Picker label did not update to expected title. expected={related_title!r} actual={actual!r}"
        )


def save_changes() -> None:
    result = chrome_exec_js(
        """(() => {
            const save = document.querySelector('#save') ||
              [...document.querySelectorAll('*')].find(
              el => (el.innerText || '').trim() === 'Save'
            );
            if (!save) return 'NO_SAVE';
            save.click();
            return 'CLICKED';
        })()"""
    )
    if result != "CLICKED":
        raise RuntimeError(f"Could not click Save: {result}")
    wait_for(
        """(() => {
            const save = document.querySelector('#save') ||
              [...document.querySelectorAll('*')].find(
              el => (el.innerText || '').trim() === 'Save'
            );
            const body = document.body ? document.body.innerText : '';
            const disabled = save ? (save.getAttribute('aria-disabled') || String(save.hasAttribute('disabled'))) : '';
            return body.includes('All changes saved') && (disabled === 'true' || disabled === 'True')
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
        f"""(() => {{
            const root = document.querySelector('#linked-video-editor-link');
            const expected = {json.dumps(expected_title)};
            const fullText = (root?.innerText || '').trim();
            if (fullText.includes(expected)) return expected;
            return root?.querySelector('.dropdown-trigger-text')?.innerText?.trim() || fullText || '';
        }})()"""
    )
    if label != expected_title:
        raise RuntimeError(
            f"Reload verification failed. expected related title {expected_title!r}, got {label!r}"
        )


def set_related_video(
    short_video_id: str,
    related_video_id: str,
    related_title: str,
    *,
    profile_directory: str = "",
    open_fresh_window: bool = False,
    close_window_on_success: bool = True,
) -> None:
    print(f"{short_video_id}: opening Studio edit page", flush=True)
    url = f"https://studio.youtube.com/video/{short_video_id}/edit"
    if open_fresh_window and profile_directory:
        launch_chrome(profile_directory, url, relaunch=False)
    else:
        chrome_navigate(url, profile_directory=profile_directory)
    time.sleep(8.0)
    ensure_page_ready(short_video_id)
    current = related_video_label(related_title)
    if current == related_title:
        close_related_video_picker()
        if has_pending_save():
            print(f"{short_video_id}: related video selected but unsaved; saving", flush=True)
            save_changes()
        verify_related_title(related_title)
        print(f"{short_video_id}: already set -> {related_title}", flush=True)
        if close_window_on_success:
            close_studio_window(short_video_id)
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
    if close_window_on_success:
        close_studio_window(short_video_id)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manager-email", default=DEFAULT_MANAGER_EMAIL)
    parser.add_argument("--profile-directory", default=DEFAULT_PROFILE_DIRECTORY)
    parser.add_argument(
        "--relaunch-chrome",
        action="store_true",
        help="Close existing Chrome processes before opening the Studio automation window.",
    )
    parser.add_argument(
        "--keep-window-open",
        action="store_true",
        help="Leave Studio edit windows open after successful related-video verification.",
    )
    parser.add_argument("--pair", action="append", default=[], help="short_id:related_id:related_title")
    args = parser.parse_args()

    if not args.pair:
        parser.error("at least one --pair is required")

    profile_directory = args.profile_directory or resolve_profile(args.manager_email)

    first_short = args.pair[0].split(":", 2)[0]
    first_url = f"https://studio.youtube.com/video/{first_short}/edit"
    launch_chrome(profile_directory, first_url, relaunch=args.relaunch_chrome)
    time.sleep(8.0)
    try:
        wait_for("""(() => document.body ? 'BODY' : '')()""", timeout_s=15.0)
    except Exception as exc:
        print(
            f"Initial Chrome readiness check failed ({exc}); opening a fresh Studio window and retrying",
            file=sys.stderr,
            flush=True,
        )
        launch_chrome(profile_directory, first_url, relaunch=False)
        time.sleep(8.0)
        wait_for("""(() => document.body ? 'BODY' : '')()""", timeout_s=20.0)

    errors = []
    needs_fresh_window = False
    for raw_pair in args.pair:
        short_id, related_id, related_title = raw_pair.split(":", 2)
        try:
            set_related_video(
                short_id,
                related_id,
                related_title,
                profile_directory=profile_directory,
                open_fresh_window=needs_fresh_window,
                close_window_on_success=not args.keep_window_open,
            )
            if not args.keep_window_open:
                needs_fresh_window = True
        except Exception as exc:
            try:
                close_related_video_picker()
            except Exception:
                pass
            print(
                f"{short_id}: ERROR related video not set -> {exc}",
                file=sys.stderr,
                flush=True,
            )
            errors.append(short_id)

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
