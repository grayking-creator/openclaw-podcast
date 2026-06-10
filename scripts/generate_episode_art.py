#!/usr/bin/env python3
"""
Generate bespoke PIL episode art module for a given episode number.

Usage:
    python3 scripts/generate_episode_art.py 030

Reads the episode show notes, generates a draw_art(img, W, H) function, tests it
renders without error, and writes:
    scripts/episode_art/episode_NNN_art.py

Uses OpenClaw's configured OpenAI image provider to generate a square visual
anchor, then writes a small Pillow draw_art() module that composites that image
into the standard cover renderer.
"""
import os, sys, subprocess, re, textwrap, importlib.util, traceback
from pathlib import Path

PODCAST_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = Path(__file__).parent
ART_DIR     = SCRIPTS_DIR / "episode_art"
ART_DIR.mkdir(exist_ok=True)
IMAGE_DIR   = PODCAST_DIR / "images"
IMAGE_DIR.mkdir(exist_ok=True)
DEFAULT_OPENAI_IMAGE_MODEL = "openai/gpt-image-2"


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
        Create square podcast cover center art for AgentStack Daily episode {ep_num:03d}.
        This is only the image layer; do not include any legible text, titles, captions,
        episode numbers, podcast names, watermarks, or UI labels. Typography will be added
        later by a local renderer.

        Episode title: {episode_title}
        Tagline: {tagline or "(none provided)"}

        Visual anchor requirement: {visual_anchor_hint}

        Style: premium technical editorial illustration, concrete recognizable central object,
        high contrast, cinematic lighting, crisp product/interface shapes, not generic sci-fi,
        not a star field, not abstract glowing dots, not a reusable dashboard wallpaper.

        Leave clean negative space near the top and bottom so local cover text can overlay later.

        Show notes summary:
        {show_notes_text[:1800]}
    """).strip()


def generate_openai_image(prompt, ep_num):
    out_path = IMAGE_DIR / f"episode_{ep_num:03d}_openai_art.png"
    model = os.getenv("OPENAI_EPISODE_ART_IMAGE_MODEL", DEFAULT_OPENAI_IMAGE_MODEL)
    cmd = [
        "openclaw", "infer", "image", "generate",
        "--model", model,
        "--size", "1024x1024",
        "--output-format", "png",
        "--output", str(out_path),
        "--timeout-ms", "300000",
        "--prompt", prompt,
    ]
    result = subprocess.run(cmd, cwd=str(PODCAST_DIR), capture_output=True, text=True, timeout=330)
    if result.returncode != 0 or not out_path.exists() or out_path.stat().st_size < 100_000:
        detail = (result.stderr or result.stdout or "no output").strip()[:1200]
        raise RuntimeError(f"OpenAI image generation failed via OpenClaw: {detail}")
    return out_path


def module_for_image(ep_num, image_name):
    return textwrap.dedent(f"""
        from pathlib import Path
        from PIL import Image, ImageDraw, ImageFilter

        def draw_art(img, W, H):
            asset_path = Path(__file__).resolve().parents[2] / "images" / "{image_name}"
            art = Image.open(asset_path).convert("RGBA")

            target_w = int(W * 0.78)
            target_h = int(H * 0.56)
            scale = max(target_w / art.width, target_h / art.height)
            resized = art.resize((int(art.width * scale), int(art.height * scale)), Image.Resampling.LANCZOS)
            left = max(0, (resized.width - target_w) // 2)
            top = max(0, (resized.height - target_h) // 2)
            art = resized.crop((left, top, left + target_w, top + target_h))

            mask = Image.new("L", (target_w, target_h), 0)
            md = ImageDraw.Draw(mask)
            md.rounded_rectangle((0, 0, target_w, target_h), radius=58, fill=218)
            edge = Image.new("L", (target_w, target_h), 0)
            ed = ImageDraw.Draw(edge)
            ed.rounded_rectangle((20, 20, target_w - 20, target_h - 20), radius=48, fill=255)
            mask = Image.composite(mask, edge.filter(ImageFilter.GaussianBlur(20)), edge)

            glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glow)
            x = (W - target_w) // 2
            y = int(H * 0.16)
            gd.rounded_rectangle((x - 30, y - 30, x + target_w + 30, y + target_h + 30), radius=76, fill=(30, 170, 210, 70))
            img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(38)))

            layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            art.putalpha(mask)
            layer.alpha_composite(art, (x, y))

            shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            sd = ImageDraw.Draw(shade)
            sd.rectangle((0, int(H * 0.66), W, H), fill=(0, 0, 0, 118))
            sd.rectangle((0, 0, W, int(H * 0.17)), fill=(0, 0, 0, 80))
            return Image.alpha_composite(Image.alpha_composite(img, layer), shade)
    """).strip() + "\n"


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

    print(f"[EP{ep_num:03d}] Generating art module...")
    prompt = build_prompt(ep_num, show_notes)
    image_path = generate_openai_image(prompt, ep_num)
    print(f"  OpenAI image generated: {image_path.name} ({image_path.stat().st_size} bytes)")
    code = module_for_image(ep_num, image_path.name)

    ok, err = test_module(code, ep_num)
    if ok:
        out = ART_DIR / f"episode_{ep_num:03d}_art.py"
        out.write_text(code, encoding="utf-8")
        print(f"[EP{ep_num:03d}] Art module written: {out}")
        return

    print(f"[EP{ep_num:03d}] Generated module failed test:\n{err}")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_episode_art.py <episode_number>")
        sys.exit(1)
    generate(int(sys.argv[1]))
