#!/usr/bin/env python3
"""
Generate bespoke PIL episode art module for a given episode number.

Usage:
    python3 scripts/generate_episode_art.py 030

Reads the episode show notes, calls Claude to produce a draw_art(img, W, H) function,
tests it renders without error, and writes:
    scripts/episode_art/episode_NNN_art.py
"""
import sys, subprocess, re, textwrap, importlib.util, traceback
from pathlib import Path

PODCAST_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = Path(__file__).parent
ART_DIR     = SCRIPTS_DIR / "episode_art"
ART_DIR.mkdir(exist_ok=True)


def find_show_notes(ep_num):
    candidates = [
        PODCAST_DIR / f"show_notes_episode_{ep_num:03d}.md",
        PODCAST_DIR / f"episodes/episode_{ep_num:03d}_transcript.md",
        PODCAST_DIR / f"episodes/episode_{ep_num:03d}_transcript_nova.md",
    ]
    for p in candidates:
        if p.exists():
            return p.read_text(encoding="utf-8")[:3000]   # first 3k chars is enough
    return None


SYSTEM = textwrap.dedent("""
You are a Python + Pillow visual designer. You write PIL/Pillow code that renders
abstract, atmospheric podcast cover art that matches the thematic content of an episode.

Rules:
- Output ONLY a Python code block — no prose, no explanation.
- The code must define exactly one function: def draw_art(img, W, H)
- img is an RGBA PIL Image (already has a background gradient painted on it).
  The function must composite art onto it and return the updated img.
- Use only: PIL (Image, ImageDraw, ImageFilter), math, random — no other imports.
- Do not draw any text — text is added by the caller.
- Keep the art in the vertical band y=150 to y=960 so it doesn't collide with title text.
- Use a helper composite() pattern:
    def composite(draw_fn, blur=0):
        nonlocal img
        layer = Image.new("RGBA", (W, H), (0,0,0,0))
        ld = ImageDraw.Draw(layer)
        draw_fn(ld)
        if blur > 0: layer = layer.filter(ImageFilter.GaussianBlur(blur))
        img = Image.alpha_composite(img, layer)
        return img
- Keep elements semi-transparent (alpha 30-220) so the background shows through.
- The scene must be visually distinct and thematically tied to the episode summary below.
- The scene must also be unmistakably tied to the episode title.
- NEVER use generic star fields, orbit rings, glowing cosmic cores, vague dashboards,
  random node clouds, or reusable "tech energy" as the central image.
- The central image must be a concrete, episode-specific object or event from the story
  slate: recognizable product surfaces, app connectors, marketplaces, documents,
  meeting tiles, devices, node editors, company-logo-inspired shapes, etc.
- If the title names a concrete object, machine, product, device, room, or interface,
  depict that thing literally and centrally.
- If the title names companies or products, use simple symbolic/geometric logo-inspired
  marks and interfaces rather than abstract blobs.
- Abstract support elements are fine only as background accents; the central anchor must
  be recognizable without any cover text being present.
- Use at most 80 composite() calls total for performance.
""").strip()


def extract_episode_title(show_notes_text, ep_num):
    title_match = re.search(r"## Episode Title\s*\n\*\*(.+?)\*\*", show_notes_text, re.DOTALL)
    if title_match:
        return title_match.group(1).strip()

    heading_match = re.search(rf"^#\s*EP{ep_num:03d}\s*[—-]\s*(.+)$", show_notes_text, re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()

    return f"Episode {ep_num}"


def extract_tagline(show_notes_text):
    tagline_match = re.search(r"## Tagline\s*\n(.+?)(?=\n## |\Z)", show_notes_text, re.DOTALL)
    if tagline_match:
        return collapse_ws(tagline_match.group(1))
    return ""


def collapse_ws(text):
    return re.sub(r"\s+", " ", text or "").strip()


def derive_visual_anchor_hint(title, tagline, show_notes_text):
    lowered = f"{title} {tagline} {show_notes_text[:1200]}".lower()

    if "project deal" in lowered or ("anthropic" in lowered and "google" in lowered):
        return "Render a concrete agent-market deal table: Anthropic-inspired bars and a Google-colored G/handshake meeting over a signed deal card, with connector/app icons around it."
    if "comfyui" in lowered:
        return "Render a recognizable node-based ComfyUI workflow canvas with connected boxes as the centered hero object."
    if "google meet" in lowered or "meet" in lowered:
        return "Render a recognizable video meeting window with participant tiles, a microphone/camera control bar, and exported transcript/attendance cards."
    if "claude" in lowered and "connector" in lowered:
        return "Render a personal-app connector hub: a Claude/Anthropic-inspired center mark connected to ride, music, grocery, travel, and tax app tiles."
    if "dgx spark" in lowered:
        return "Render an unmistakable DGX Spark style compact AI workstation as the centered hero object."
    if "chrome" in lowered or "browser" in lowered:
        return "Render a recognizable browser window with tabs and an address bar as the centered hero object."
    if "codex" in lowered and "surface" in lowered:
        return "Render a recognizable software work surface or coding interface, not abstract rings."
    if "release" in lowered or re.search(r"\bv20\d{2}\.", lowered):
        return "Render a recognizable release/operator control panel with concrete UI controls, meeting/browser artifacts, and status cards; do not use a star system or glowing generic core."
    if "cluster" in lowered or "gpu" in lowered or "cuda" in lowered:
        return "Render literal compute hardware or node topology as the centered object, not just glowing dots."
    if "agent" in lowered:
        return "Render a concrete tool surface or operator interface where agents act, not a generic sci-fi scene."
    return "Pick one concrete visual anchor from the title and make it the obvious centered object."


def build_prompt(ep_num, show_notes_text):
    episode_title = extract_episode_title(show_notes_text, ep_num)
    tagline = extract_tagline(show_notes_text)
    visual_anchor_hint = derive_visual_anchor_hint(episode_title, tagline, show_notes_text)
    return textwrap.dedent(f"""
        Episode number: {ep_num}

        Episode title:
        {episode_title}

        Tagline:
        {tagline or "(none provided)"}

        Visual anchor requirement:
        {visual_anchor_hint}

        Show notes summary (first 3000 chars):
        ---
        {show_notes_text}
        ---

        Write the Python draw_art function.
        The cover must read visually even with all text removed, and the center object
        should feel like the literal noun phrase from the title.
        Output only the code block.
    """).strip()


def call_claude(prompt):
    """Call claude CLI in print mode and return stdout."""
    result = subprocess.run(
        ["claude", "-p", "--model", "claude-sonnet-4-6"],
        input=f"{SYSTEM}\n\n{prompt}",
        capture_output=True,
        text=True,
        timeout=300,
    )
    if result.returncode != 0:
        raise RuntimeError(f"claude CLI failed: {result.stderr[:500]}")
    return result.stdout


def extract_code(response):
    """Pull the Python code block out of the response."""
    m = re.search(r"```python\s*(.*?)```", response, re.DOTALL)
    if m:
        return m.group(1).strip()
    # If no fences, take everything that looks like Python
    lines = [l for l in response.splitlines() if l.strip() and not l.startswith("#!")]
    return "\n".join(lines).strip()


def test_module(code_str, ep_num):
    """Write to a tmp file, import it, call draw_art on a blank image."""
    from PIL import Image
    tmp = ART_DIR / f"_test_{ep_num:03d}.py"
    tmp.write_text(code_str, encoding="utf-8")
    try:
        spec = importlib.util.spec_from_file_location("_test_art", tmp)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        blank = Image.new("RGBA", (1400, 1400), (10, 10, 20, 255))
        result = mod.draw_art(blank, 1400, 1400)
        assert result is not None, "draw_art returned None"
        return True, None
    except Exception:
        return False, traceback.format_exc()
    finally:
        tmp.unlink(missing_ok=True)


def generate(ep_num, retry=2):
    show_notes = find_show_notes(ep_num)
    if not show_notes:
        print(f"[!] No show notes found for EP{ep_num:03d}. Aborting.")
        sys.exit(1)

    print(f"[EP{ep_num:03d}] Calling Claude to generate art module...")
    prompt = build_prompt(ep_num, show_notes)

    for attempt in range(1, retry + 2):
        raw = call_claude(prompt)
        code = extract_code(raw)
        print(f"  Attempt {attempt}: got {len(code)} chars of code.")

        ok, err = test_module(code, ep_num)
        if ok:
            out = ART_DIR / f"episode_{ep_num:03d}_art.py"
            out.write_text(code, encoding="utf-8")
            print(f"[EP{ep_num:03d}] Art module written: {out}")
            return
        else:
            print(f"  Test failed:\n{err}")
            if attempt <= retry:
                print(f"  Retrying with error context...")
                prompt += f"\n\nPrevious attempt had this runtime error — fix it:\n{err[:800]}"

    print(f"[EP{ep_num:03d}] All attempts failed. Check output above.")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_episode_art.py <episode_number>")
        sys.exit(1)
    generate(int(sys.argv[1]))
