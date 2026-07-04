#!/usr/bin/env python3
"""Validate that every <enclosure> audio URL in a podcast feed actually exists.

Added 2026-06-05 after EP63 was committed to all five feeds while its EN audio
had never been uploaded — the enclosure URL
  https://clawdassistant85-netizen.github.io/openclaw-podcast-media-en/audio/episode_063.mp3
returned 404 (the op3.dev wrapper just 302-redirects to that 404). The episode
was "approved but unpublished": approval gated the *audio review*, not the
*published artifact*, so a dead-audio entry reached the live feed.

This is the real guard for "an unpublished episode must never be in the feeds":
a feed item is only publishable if its audio is fetchable (HTTP 200).

Definitive HTTP errors (>=400) BLOCK. Network/timeout errors only WARN (so the
check can't be defeated by transient offline conditions, and a flaky network
doesn't block an otherwise-valid commit). Skip entirely with
FEED_SKIP_ENCLOSURE_CHECK=1.

Exit codes:
  0  all enclosures reachable (or only soft network warnings)
  3  at least one enclosure returned a definitive HTTP error (missing audio)

Usage:
  validate_feed_enclosures.py feed.xml translations/feed_*.xml
"""
import os
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

TIMEOUT = 12
UA = "openclaw-feed-enclosure-check/1.0"


def _status(url, method):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    # add a 1-byte range so a GET fallback doesn't pull whole MP3s
    if method == "GET":
        req.add_header("Range", "bytes=0-0")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return resp.status  # urllib follows redirects (incl. op3 302) automatically


def check_url(url):
    """Return (ok: bool, detail: str, soft: bool).

    soft=True means we could not get a definitive answer (network error) and the
    caller should warn rather than block.

    Locked 2026-06-29, EP076 incident: op3.dev can transiently 404 on a cold
    cache hit even when the underlying GitHub release URL is live. To avoid
    a one-shot flake blocking publish on a real-life-good URL, retry any
    non-2xx transient HTTP error with a brief backoff. Sustained real 404s
    still block. Headless network issues remain soft.
    """
    import time
    transient_codes = {404, 502, 503, 504}
    last_code = None
    last_detail = "no usable response"
    for attempt in range(3):
        for method in ("HEAD", "GET"):
            try:
                code = _status(url, method)
                if 200 <= code < 400:
                    return (True, f"HTTP {code}", False)
                last_code = code
                last_detail = f"HTTP {code}"
                if last_code in transient_codes:
                    # wait briefly and retry — op3 cache or CDN hiccup
                    time.sleep(2 + attempt)
                    continue
                return (False, last_detail, False)
            except urllib.error.HTTPError as e:
                if e.code in (403, 405, 501) and method == "HEAD":
                    continue
                last_code = e.code
                last_detail = f"HTTP {e.code}"
                if last_code in transient_codes:
                    time.sleep(2 + attempt)
                    continue
                return (False, last_detail, False)
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                return (True, f"network error ({e}) — not verified", True)
    return (False, last_detail, False)


def enclosure_urls(path):
    root = ET.parse(path).getroot()
    out = []
    for item in root.iter("item"):
        ep = item.findtext("{http://www.itunes.com/dtds/podcast-1.0.dtd}episode") or "?"
        enc = item.find("enclosure")
        if enc is not None and enc.get("url"):
            out.append((ep, enc.get("url")))
    return out


def main(argv):
    files = argv[1:]
    if not files:
        print("usage: validate_feed_enclosures.py <feed.xml> [more.xml ...]", file=sys.stderr)
        return 1
    if os.environ.get("FEED_SKIP_ENCLOSURE_CHECK") == "1":
        print("⏭️  enclosure check skipped (FEED_SKIP_ENCLOSURE_CHECK=1)")
        return 0
    failed = False
    for path in files:
        try:
            enclosures = enclosure_urls(path)
        except (ET.ParseError, FileNotFoundError) as e:
            print(f"⚠️  {path}: {e} — skipping enclosure check", file=sys.stderr)
            continue
        for ep, url in enclosures:
            ok, detail, soft = check_url(url)
            if ok and soft:
                print(f"⚠️  {path} EP{ep}: {detail}: {url}", file=sys.stderr)
            elif ok:
                print(f"✅ {path} EP{ep}: {detail}")
            else:
                failed = True
                print(f"🚫 {path} EP{ep}: audio missing — {detail}: {url}", file=sys.stderr)
    if failed:
        print(
            "\nRefusing to publish: a feed item points to audio that does not exist "
            "(the EP63 missing-audio incident). Upload the audio, or remove the item, "
            "before committing the feed.",
            file=sys.stderr,
        )
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
