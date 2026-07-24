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
import os, sys, subprocess, re, textwrap, importlib.util, time, traceback
from pathlib import Path

PODCAST_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = Path(__file__).parent
ART_DIR     = SCRIPTS_DIR / "episode_art"
ART_DIR.mkdir(exist_ok=True)
IMAGE_DIR   = PODCAST_DIR / "images"
IMAGE_DIR.mkdir(exist_ok=True)
DEFAULT_OPENAI_IMAGE_MODEL = "openai/gpt-image-2"
# Tried in order after the primary model fails all its attempts.
# minimax/image-01: no --size (use --aspect-ratio), ignores png hint, always writes JPEG.
FALLBACK_IMAGE_MODELS = ["minimax/image-01"]


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

    inline_match = re.search(r"^\*\*Title:\*\*\s*(.+?)\s*$", show_notes_text, re.MULTILINE)
    if inline_match:
        return collapse_ws(inline_match.group(1))

    heading_match = re.search(
        rf"^#\s*(?:AgentStack Daily\s+)?EP{ep_num:03d}\s*[—-]\s*(.+)$",
        show_notes_text,
        re.MULTILINE | re.IGNORECASE,
    )
    if heading_match:
        return heading_match.group(1).strip()

    return f"Episode {ep_num}"


def extract_tagline(show_notes_text):
    tagline_match = re.search(r"## Tagline\s*\n(.+?)(?=\n## |\Z)", show_notes_text, re.DOTALL)
    if tagline_match:
        return collapse_ws(tagline_match.group(1))
    inline_match = re.search(r"^\*\*Tagline:\*\*\s*(.+?)\s*$", show_notes_text, re.MULTILINE)
    if inline_match:
        return collapse_ws(inline_match.group(1))
    return ""


def collapse_ws(text):
    return re.sub(r"\s+", " ", text or "").strip()


def art_context_without_episode_branding(show_notes_text, ep_num):
    """Keep story context while withholding episode/podcast branding from the image model."""
    cleaned = re.sub(r"^#.*$", "", show_notes_text, count=1, flags=re.MULTILINE)
    cleaned = re.sub(r"^\*\*(?:Title|Tagline):\*\*.*$", "", cleaned, flags=re.MULTILINE)
    cleaned = re.sub(rf"\bEP\s*0*{ep_num}\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(rf"\bEpisode\s+0*{ep_num}\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\bAgentStack Daily\b", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def extract_weighted_story_context(show_notes_text, ep_num):
    """Give the image model the full slate's editorial choices without prompt bloat."""
    slate = re.search(
        r"## Story Slate\s*(.+?)(?=\n## (?:Model Discovery|Local LLM|GitHub|Source|Links)|\Z)",
        show_notes_text,
        re.DOTALL | re.IGNORECASE,
    )
    source = slate.group(1) if slate else show_notes_text
    entries = re.findall(
        r"^\d+\.\s+\*\*(.+?)\*\*\s*\n(.+?)(?=^\d+\.\s+\*\*|\Z)",
        source,
        re.MULTILINE | re.DOTALL,
    )
    if not entries:
        # No "## Story Slate" match means `source` is the raw show notes text,
        # which still carries the episode/podcast branding header — strip it.
        return collapse_ws(art_context_without_episode_branding(source, ep_num))[:6000]
    briefs = []
    for index, (heading, body) in enumerate(entries, 1):
        first_paragraph = re.split(r"\n(?:Technical depth|Actionability|Listener hook)", body, 1)[0]
        briefs.append(f"Story {index}: {collapse_ws(heading)} — {collapse_ws(first_paragraph)[:420]}")
    return "\n".join(briefs)[:8000]


def derive_visual_anchor_hint(title, tagline, show_notes_text):
    lowered = f"{title} {tagline} {show_notes_text[:1200]}".lower()

    if "kimi k3" in lowered:
        return (
            "Start from Kimi K3 as the headline priority, then weigh the full slate for the most "
            "distinctive supporting visual. Kimi's lunar/crescent identity and the Ternary-Bonsai "
            "story can form one unusually coherent scene: a monumental artificial moon illuminating "
            "a compact neural bonsai, with scale contrast suggesting 2.8 trillion parameters versus "
            "a compressed local model. Treat this as an editorial concept, not a required logo-plus-object collage. "
            "Do not use a control panel, server rack, circuitry wall, dashboard, gauge, robot, "
            "glowing mystery core, or other generic AI machinery."
        )
    if "gpt-5.6 sol" in lowered and "bonsai 27b" in lowered:
        return (
            "Make GPT-5.6 Sol's finished-work capability the dominant subject: show one concrete "
            "software task moving through tool use into a visibly completed deliverable with a "
            "clear completion mark. Beside it, show Bonsai 27B running locally on a real smartphone "
            "with a compact 3.9 GB memory motif, and an AMD desktop workstation with four populated "
            "memory banks representing 128 GB unified memory. Include a smaller screen-operation cue "
            "for Gemini 3.5 Flash. Use these literal product mechanisms instead of a glowing core, "
            "server skyline, power grid, generic dashboard, or abstract data streams."
        )
    if "terrazero" in lowered:
        return (
            "Build the scene around TerraZero: a clearly recognizable autonomous car learning "
            "from scratch inside a procedural multi-lane city-driving simulator, with many "
            "parallel trajectory traces accelerating toward a 1.3-million-steps-per-second "
            "throughput motif. Integrate PalmClaw as a real smartphone running an on-device agent, "
            "and visualize Estimate-Execute-Expand as a compact three-stage code pipeline that "
            "shrinks a large token stream by 91 percent. These must read as one episode-specific "
            "editorial composition, not as a generic control desk or robot dashboard."
        )
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
    art_context = art_context_without_episode_branding(show_notes_text, ep_num)
    weighted_story_context = extract_weighted_story_context(show_notes_text, ep_num)
    return textwrap.dedent(f"""
        Create a square technical editorial illustration for a podcast cover.
        This is only the image layer; do not include any legible text, titles, captions,
        episode numbers, podcast names, watermarks, or UI labels. Typography will be added
        later by a local renderer.

        Story title: {episode_title}
        Tagline: {tagline or "(none provided)"}

        Make an editorial concept decision before composing. Weight the title/headline at roughly
        55 percent. Rank the full story slate for the remaining weight using listener importance,
        novelty, visual distinctiveness, concrete imagery, and whether a story can reinforce the
        headline inside one coherent scene. Use at most one or two supporting story cues. Do not
        illustrate every story, do not follow rundown order, and do not create a checklist collage.
        Routine harness releases should receive effectively zero visual weight unless named in the title.

        Visual anchor requirement: {visual_anchor_hint}

        Translate the strongest proper nouns, mechanisms, scale contrast, and quantitative hooks
        into one memorable visual metaphor. The finished image must be identifiable from this
        episode's title and weighted slate, not merely from generic AI aesthetics.
        Do not substitute a generic AI dashboard, robot arm, glowing core, server console, or
        interchangeable agent-network scene. Use at least two title-specific visual cues, with
        the headline subject as the dominant cue. Do not invent brand logos.

        Style: premium technical editorial illustration, concrete recognizable central object,
        high contrast, cinematic lighting, crisp product/interface shapes, not generic sci-fi,
        not a star field, not abstract glowing dots, not a reusable dashboard wallpaper.

        Leave clean negative space near the top and bottom so local cover text can overlay later.

        Full weighted story slate:
        {weighted_story_context}

        Additional opening context:
        {art_context[:1200]}
    """).strip()


def _image_cmd_and_path(model, prompt, ep_num):
    provider = model.split("/", 1)[0]
    if provider == "minimax":
        out_path = IMAGE_DIR / f"episode_{ep_num:03d}_{provider}_art.jpg"
        extra = ["--aspect-ratio", "1:1"]
    else:
        out_path = IMAGE_DIR / f"episode_{ep_num:03d}_{provider}_art.png"
        extra = ["--size", "1024x1024", "--output-format", "png"]
    cmd = [
        "openclaw", "infer", "image", "generate",
        "--model", model,
        *extra,
        "--output", str(out_path),
        "--timeout-ms", "300000",
        "--prompt", prompt,
    ]
    return cmd, out_path


def generate_episode_image(prompt, ep_num):
    primary = os.getenv("OPENAI_EPISODE_ART_IMAGE_MODEL", DEFAULT_OPENAI_IMAGE_MODEL)
    candidates = [(primary, 3)] + [(m, 2) for m in FALLBACK_IMAGE_MODELS if m != primary]
    failures = []
    for model, attempts in candidates:
        cmd, out_path = _image_cmd_and_path(model, prompt, ep_num)
        last_detail = "no output"
        for attempt in range(1, attempts + 1):
            try:
                result = subprocess.run(cmd, cwd=str(PODCAST_DIR), capture_output=True, text=True, timeout=330)
                if result.returncode == 0 and out_path.exists() and out_path.stat().st_size >= 100_000:
                    return out_path
                last_detail = (result.stderr or result.stdout or "no output").strip()[:1200]
            except subprocess.TimeoutExpired:
                last_detail = f"openclaw infer timed out after 330s (attempt {attempt}/{attempts})"
            if attempt < attempts:
                delay = 15 * attempt
                print(f"  [!] {model} attempt {attempt}/{attempts} failed: {last_detail.splitlines()[-1] if last_detail else last_detail}")
                print(f"      Retrying in {delay}s...")
                time.sleep(delay)
        failures.append(f"{model}: {last_detail}")
        print(f"  [!] {model} exhausted after {attempts} attempts; trying next provider...")
    raise RuntimeError(
        "Episode art image generation failed on all providers via OpenClaw: "
        + " | ".join(failures)
    )


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


def generate(ep_num):
    show_notes = find_show_notes(ep_num)
    if not show_notes:
        print(f"[!] No show notes found for EP{ep_num:03d}. Aborting.")
        sys.exit(1)

    print(f"[EP{ep_num:03d}] Generating art module...")
    prompt = build_prompt(ep_num, show_notes)
    image_path = generate_episode_image(prompt, ep_num)
    print(f"  Image generated: {image_path.name} ({image_path.stat().st_size} bytes)")
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
