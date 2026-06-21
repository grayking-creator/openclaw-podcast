#!/usr/bin/env python3
"""Recover a failed lane_translations step on the approved-release orchestrator.

What this fixes (the EP072-style failure):
  1. translate_metadata produced a title whose body after the "{prefix} {ep}:"
     prefix was still English (model returned only the localized prefix). The
     translated feed entry got written, but phase_qc flagged it as
     "Title NOT translated" and the orchestrator died.
  2. The morning pipeline then re-ran the FULL pipeline for the same episode
     because the show notes were still on disk and QC passed, and the release
     state said "failed" but the collision check didn't see it.

What this script does:
  1. Reads release_ep{ep:03d}_state.json. Verifies lane_translations is the
     failed lane (or recovers any failed lane).
  2. Re-runs translate_metadata with the strengthened prompt for every language
     whose translated title body still equals the English body (or, for non-Latin
     scripts, is missing the script-native characters).
  3. Patches the existing translations/feed_{lang}.xml entries in place via
     update_translated_feed_entry (no re-insert — duplicates would be rejected).
  4. Re-runs phase_qc, phase_cdn, phase_publish_translations.
  5. Marks lane_translations complete in the orchestrator state, clears
     run_status=failed, and post a build-log line saying recovery succeeded.

What this does NOT do:
  - It does NOT touch the EN release (already published). If EN publish hasn't
    completed, this script refuses and tells you to use --from-step on the
    orchestrator instead.
  - It does NOT regenerate show notes, transcripts, audio, or cover art — those
    were good. Only the metadata-title + feed-entry fields are touched.

Usage:
  python3 scripts/recover_failed_translation_lane.py <ep_num>
  python3 scripts/recover_failed_translation_lane.py 72            # explicit

Exit codes:
  0 = recovered successfully
  1 = nothing to do (lane_translations already complete or no failure)
  2 = refused (EN publish not complete, or no release state file)
  3 = recovery ran but phase_qc still failed — investigate model output
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import release_episode as rel
from release_episode_approved import (
    STEP_EN_PUBLISH,
    STEP_TRANSLATIONS,
    completed_steps,
    mark_lane_result,
    mark_run_status,
    mark_step_complete,
    post_build_log,
    save_state,
)


SCRIPTS_DIR = Path(__file__).resolve().parent
PODCAST_DIR = SCRIPTS_DIR.parent
LANGS = ("es", "de", "pt", "hi")


def log(msg: str) -> None:
    print(msg)


def find_failed_lanes(state: dict) -> list[str]:
    meta = state.get("approved_orchestrator", {})
    lane_results = meta.get("lane_results", {})
    return [
        lane for lane, payload in lane_results.items()
        if isinstance(payload, dict) and payload.get("status") == "failed"
    ]


def title_body_is_english(translated_title: str, en_title: str) -> bool:
    import re
    if not translated_title or not en_title:
        return False
    m = re.match(r"^.+?\s+\d+\s*[:\-–]\s*(.+)$", translated_title.strip())
    body = (m.group(1) if m else translated_title).strip()
    return re.sub(r"\s+", " ", body.lower()) == re.sub(r"\s+", " ", en_title.strip().lower())


def title_missing_native_script(translated_title: str, lang: str) -> bool:
    import re
    if lang != "hi":
        return False
    if not translated_title:
        return True
    return not re.search(r"[\u0900-\u097F]", translated_title)


def retranslate_if_needed(ep_num: int, state: dict) -> list[str]:
    """Re-translate metadata for any language whose title body is still English
    or missing its native script. Returns list of re-translated languages."""
    from release_episode import (
        extract_episode_title,
        TITLE_PREFIXES,
    )
    show_notes_path = PODCAST_DIR / f"show_notes_episode_{ep_num:03d}.md"
    notes = show_notes_path.read_text()
    en_title = extract_episode_title(notes, ep_num)
    translations = state.setdefault("translations", {})

    re_translated = []
    for lang in LANGS:
        meta = translations.get(lang, {}).get("meta", {})
        title = meta.get("title", "")
        needs = title_body_is_english(title, en_title) or title_missing_native_script(title, lang)
        if not needs:
            log(f"  ✅ [{lang}] title looks translated: {title!r}")
            continue
        log(f"  ⚠️  [{lang}] re-translating metadata (was: {title!r})")
        new_meta = rel.translate_metadata(ep_num, lang)
        translations.setdefault(lang, {})["meta"] = new_meta
        translations[lang]["done"] = True
        re_translated.append(lang)
    state["translations"] = translations
    save_state(ep_num, state)
    return re_translated


def update_existing_feed_entries(ep_num: int, state: dict, langs: list[str]) -> int:
    """Update existing feed entries in place with the corrected metadata.
    Returns count of feeds actually modified."""
    translations = state.get("translations", {})
    updated = 0
    for lang in langs:
        meta = translations.get(lang, {}).get("meta", {})
        new_title = meta.get("title", "")
        new_desc = meta.get("description", "")
        if not new_title:
            continue
        if rel.update_translated_feed_entry(
            ep_num, lang, title=new_title, description=new_desc or None
        ):
            updated += 1
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Recover a failed lane_translations step (EP072-style)"
    )
    parser.add_argument("episode", type=int, help="Episode number (e.g. 72)")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would happen without modifying any state or feed XML",
    )
    args = parser.parse_args()
    ep_num = args.episode
    ep_str = f"{ep_num:03d}"

    state = rel.load_state(ep_num)
    meta = state.get("approved_orchestrator", {})
    completed = completed_steps(state)
    failed_lanes = find_failed_lanes(state)

    log(f"\n{'=' * 68}")
    log(f"EP{ep_str} — Failed Translation Lane Recovery")
    log(f"{'=' * 68}")

    # Guard: refuse if EN publish hasn't completed (this script only fixes
    # translation metadata + feed entries; the EN side must already be live).
    if STEP_EN_PUBLISH not in completed:
        log(
            f"❌ Refused: EN publish ({STEP_EN_PUBLISH}) hasn't completed yet.\n"
            "  This script only recovers the translation lane.\n"
            f"  Use: python3 scripts/release_episode_approved.py {ep_num} --from-step {STEP_TRANSLATIONS}"
        )
        return 2

    if STEP_TRANSLATIONS in completed and not failed_lanes:
        log(f"ℹ️  Nothing to recover: lane_translations already complete, no failed lanes.")
        return 1

    if failed_lanes and STEP_TRANSLATIONS not in failed_lanes:
        log(
            f"⚠️  Different lane(s) failed: {', '.join(failed_lanes)}. "
            "This script only fixes lane_translations; rerun the orchestrator "
            f"with --from-step for the actual failed lane."
        )
        return 1

    log(f"  Detected failed lane: lane_translations")
    log(f"  Failure: {meta.get('failure', '(no detail)')}")

    if args.dry_run:
        log("\n  --dry-run: would re-translate metadata, update feed entries, re-run QC.")
        return 0

    # Step 1: re-translate
    log(f"\n[1/4] Re-translating metadata for languages with English title body...")
    re_translated = retranslate_if_needed(ep_num, state)
    if not re_translated:
        log("  ℹ️  No language needed re-translation (titles already correct).")
    else:
        log(f"  → Re-translated: {', '.join(re_translated).upper()}")

    # Step 2: patch existing feed entries
    log(f"\n[2/4] Patching existing feed entries in place...")
    modified = update_existing_feed_entries(ep_num, state, list(LANGS))
    log(f"  → {modified} feed(s) modified.")

    # Step 3: re-run phase_qc
    log(f"\n[3/4] Re-running phase_qc...")
    try:
        rel.phase_qc(ep_num, state)
        log("  ✅ phase_qc passed")
    except Exception as exc:
        log(f"  ❌ phase_qc STILL FAILING: {exc}")
        log("  Inspect /tmp/show_notes_build.log and check the model's output.")
        return 3

    # Step 4: phase_cdn + phase_publish_translations
    log(f"\n[4/4] Pushing translated CDN assets and website...")
    state = rel.phase_cdn(ep_num, state)
    state = rel.phase_publish_translations(ep_num, state)

    # Mark lane_translations complete in the orchestrator state
    mark_step_complete(ep_num, state, STEP_TRANSLATIONS)
    mark_lane_result(state, STEP_TRANSLATIONS, "complete", {
        "recovered_via": "recover_failed_translation_lane.py",
        "recovered_at": datetime.now(timezone.utc).isoformat(),
        "re_translated_langs": re_translated,
    })
    # Clear the failed status from the meta record
    meta = state.get("approved_orchestrator", {})
    if meta.get("run_status") == "failed":
        meta["run_status"] = "running"
    meta.pop("failure", None)
    meta["last_recovery"] = "recover_failed_translation_lane.py"
    save_state(ep_num, state)
    post_build_log(ep_num, f"✅ lane_translations recovered via recover_failed_translation_lane.py")

    log(f"\n{'=' * 68}")
    log(f"✅ EP{ep_str} lane_translations recovered.")
    log(f"   Re-translated: {', '.join(re_translated).upper() or 'none needed'}")
    log(f"   Feeds updated: {modified}")
    log(f"   Phase QC + CDN + publish_translations: complete")
    log(f"\nNext steps (manual or via orchestrator --from-step):")
    log(f"   python3 scripts/release_episode_approved.py {ep_num} --from-step post_translation --pub-date '<original pub_date>'")
    log(f"   ... or just re-run: python3 scripts/launch_approved_release.py {ep_num} --pub-date '<original pub_date>'")
    log(f"   (orchestrator will skip completed steps and continue from post_translation → youtube → discord)")
    log(f"{'=' * 68}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
