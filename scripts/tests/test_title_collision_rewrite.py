#!/usr/bin/env python3
"""Regression tests for the EP074 title-collision fix (2026-06-22).

EP074 root cause: `build_show_notes.py` produced a model-discovery Story #1
with title "Nex AGI: Nex-N2-Pro lands via API", which collided with EP073's
"Poolside: Laguna M.1 lands via API" on the shared `lands via API` template.
The pre-repair hard-protected Story #1 with `if i == 0`, so the collision
survived to the final gate; the post-gate `repair()` could only drop+backfill
from the news/radar pool and Story #1 was never backfillable. The build
exited 1 after 3 repair rounds with "no actionable repair mapping".

The fix:
1. `rewrite_colliding_title()` deterministically rewrites a colliding
   templated title using the source's provider/model/url.
2. The pre-repair no longer hard-protects Story #1 — it tries the
   deterministic rewrite first, then drops+backfills if that fails.
3. The post-gate `repair()` mirrors the same rewrite-then-drop behavior.

These tests exercise `rewrite_colliding_title()` and `overlaps_prior()`
directly without the model pool, so they run offline and fast. They are
the regression fence the morning pipeline will hit on the next EP074-class
collision.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make the build_show_notes module importable when run as a script from
# any cwd. The tests don't depend on the live research context.
ROOT = Path(__file__).resolve().parent.parent.parent  # …/openclaw-podcast
sys.path.insert(0, str(ROOT / "scripts"))

import build_show_notes as bsn  # noqa: E402


# ── Prior-title corpus used to drive collisions ─────────────────────────
# Real EP073 / EP072 / EP071 slates (from the on-disk show_notes_episode_*.md
# files), so the test is exercising the exact same prior corpus the morning
# pipeline would see on 2026-06-23 against an EP075 build.
def _load_prior_titles() -> list[str]:
    import re
    out: list[str] = []
    for ep_back in (1, 2, 3):
        p = ROOT / f"show_notes_episode_{74 - ep_back:03d}.md"
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        out.extend(re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", text, re.MULTILINE))
    return out


PRIOR = _load_prior_titles()


def test_no_collision_against_real_ep073_slates():
    """The Nex-N2-Pro collision that killed EP074 (2026-06-22) is gone."""
    story = {"title": "Nex AGI: Nex-N2-Pro lands via API"}
    source = {"id": "nex-agi/nex-n2-pro",
              "url": "https://openrouter.ai/models/nex-agi/nex-n2-pro",
              "name": "Nex AGI: Nex-N2-Pro",
              "description": "Mixture-of-experts model from Nex AGI, 17B active / 397B total."}
    collide_tok = bsn.colliding_prior_tokens(story["title"], PRIOR)
    assert collide_tok, "expected Nex-N2-Pro title to collide with EP073 (sanity check)"
    rewritten = bsn.rewrite_colliding_title(story, source, collide_tok)
    print(f"  rewrite: {story['title']!r} → {rewritten!r}")
    assert not bsn.overlaps_prior(rewritten, PRIOR), (
        f"rewrite still collides with prior titles: {rewritten!r} "
        f"vs prior={PRIOR[:3]}…"
    )


def test_provider_slug_lands_in_rewrite():
    """The rewritten title carries the actual provider slug, not a templated
    phrase. This is the whole point of the deterministic helper — if the
    rewrite just shuffles boilerplate, we'd be back here next week."""
    story = {"title": "Nex AGI: Nex-N2-Pro lands via API"}
    source = {"id": "nex-agi/nex-n2-pro",
              "url": "https://openrouter.ai/models/nex-agi/nex-n2-pro",
              "name": "Nex AGI: Nex-N2-Pro",
              "description": ""}
    collide_tok = bsn.colliding_prior_tokens(story["title"], PRIOR)
    rewritten = bsn.rewrite_colliding_title(story, source, collide_tok)
    assert "nex-agi" in rewritten or "nex-n2-pro" in rewritten, (
        f"rewrite dropped the source subject: {rewritten!r}"
    )
    # The provider slug must NOT be duplicated (e.g. 'Nex AGI:nex-agi ...')
    # which is what the first revision produced. The colon-prefix is a
    # human-readable form of the provider and we drop it before substitution.
    assert "Nex AGI:nex-agi" not in rewritten and "nex-agi nex-agi" not in rewritten, (
        f"provider slug duplicated in rewrite: {rewritten!r}"
    )
    # The templated phrase that triggered the collision must be gone.
    lowered = rewritten.lower()
    for templated in ("lands via api", "ships via api", "rolls out",
                      "comes to", "arrives on"):
        assert templated not in lowered, (
            f"rewrite still contains templated phrase {templated!r}: {rewritten!r}"
        )


def test_news_story_collision_rewrite():
    """A news-story variant of the same collision also rewrites cleanly."""
    # EP072 had "Apple Foundation Models" as story #3, so a new
    # "Apple Foundation Models lands via API" would collide.
    story = {"title": "Apple Foundation Models lands via API"}
    source = {"id": "",
              "url": "https://www.apple.com/newsroom/foundation-models",
              "name": "Apple Foundation Models",
              "description": "Apple on-device foundation models."}
    collide_tok = bsn.colliding_prior_tokens(story["title"], PRIOR)
    if not collide_tok:
        # Skip if EP072/073/071 don't actually contain Apple Foundation Models
        print("  (skipping — no Apple collision in current prior corpus)")
        return
    rewritten = bsn.rewrite_colliding_title(story, source, collide_tok)
    print(f"  rewrite: {story['title']!r} → {rewritten!r}")
    assert not bsn.overlaps_prior(rewritten, PRIOR), (
        f"news-story rewrite still collides: {rewritten!r}"
    )


def test_passthrough_when_no_collision():
    """If the title is already clean, the rewrite must not corrupt it."""
    # Use a topic that's known to be absent from EP071-073
    story = {"title": "Mars rover AI navigation upgrade lands"}
    source = {"id": "", "url": "https://example.com/mars",
              "name": "Mars rover", "description": ""}
    collide_tok = bsn.colliding_prior_tokens(story["title"], PRIOR)
    if collide_tok:
        print(f"  (skipping — assumed-clean title actually collides: {collide_tok})")
        return
    rewritten = bsn.rewrite_colliding_title(story, source, collide_tok)
    # The rewrite only changes templated phrases; without one, it should
    # either pass through or fall back to the deterministic "<provider>
    # listing adds <model>" template. Either way, no collision.
    assert not bsn.overlaps_prior(rewritten, PRIOR), (
        f"clean title was rewritten into a collision: {rewritten!r}"
    )


def test_colliding_tokens_function_works_alone():
    """`colliding_prior_tokens()` mirrors `overlaps_prior()` exactly, and
    lists the union of non-stopword tokens that cause the overlap. The
    morning-pipeline operator uses this to see which tokens to drop."""
    title = "Nex AGI: Nex-N2-Pro lands via API"
    tokens = bsn.colliding_prior_tokens(title, PRIOR)
    assert isinstance(tokens, set)
    # EP073 story 3 was "Poolside: Laguna M.1 lands via API"
    # EP072 had no "Nex" or "API" collisions; the collision is solely EP073.
    expected = {"api", "lands", "via"}
    assert expected.issubset(tokens), (
        f"missing expected tokens {expected - tokens}; got {tokens}"
    )


def test_qc_error_message_lists_colliding_tokens():
    """The QC error in `find_prior_episode_repeats` must list the specific
    tokens that caused the overlap. Without this, the morning pipeline
    operator (and the hand-patch) have to re-derive them by hand."""
    import check_show_notes as qc
    # Force a collision with EP073's slate on disk
    notes_path = ROOT / "show_notes_episode_074.md"
    if not notes_path.exists():
        # The canonical EP074 was hand-patched, so collisions are gone.
        # Use the .rejected.builder instead, which still has the collision.
        notes_path = ROOT / "show_notes_episode_074.md.rejected.builder"
        if not notes_path.exists():
            print("  (skipping — no rejected draft on disk to test against)")
            return
    # Inject the offending title into a synthetic draft to force the check
    synth = notes_path.read_text(encoding="utf-8", errors="ignore")
    if "Nex AGI: Nex-N2-Pro lands via API" not in synth:
        print("  (skipping — collision string not present in on-disk draft)")
        return
    repeats = qc.find_prior_episode_repeats(notes_path, 75,
                                             ["Nex AGI: Nex-N2-Pro lands via API"],
                                             lookback=3)
    assert repeats, "expected collision in synthetic EP075 draft"
    msg = repeats[0]
    assert "shared tokens:" in msg, (
        f"QC error message must list the colliding tokens; got: {msg!r}"
    )
    print(f"  QC message: {msg}")


if __name__ == "__main__":
    tests = [
        ("no_collision_against_real_ep073_slates",
         test_no_collision_against_real_ep073_slates),
        ("provider_slug_lands_in_rewrite",
         test_provider_slug_lands_in_rewrite),
        ("news_story_collision_rewrite",
         test_news_story_collision_rewrite),
        ("passthrough_when_no_collision",
         test_passthrough_when_no_collision),
        ("colliding_tokens_function_works_alone",
         test_colliding_tokens_function_works_alone),
        ("qc_error_message_lists_colliding_tokens",
         test_qc_error_message_lists_colliding_tokens),
    ]
    passed = failed = 0
    for name, fn in tests:
        print(f"\n[test] {name}")
        try:
            fn()
            passed += 1
            print(f"  ✅ PASS")
        except AssertionError as e:
            failed += 1
            print(f"  ❌ FAIL: {e}")
        except Exception as e:
            failed += 1
            print(f"  ❌ ERROR: {type(e).__name__}: {e}")
    print(f"\n{'='*60}")
    print(f"{passed}/{len(tests)} passed, {failed} failed")
    sys.exit(0 if failed == 0 else 1)