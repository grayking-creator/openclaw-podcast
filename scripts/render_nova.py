#!/usr/bin/env python3
"""
Render transcript → nova.md for TTS generation.
Always run this fresh before generating audio — never use a stale render.
"""
import re
import sys
import argparse
from pathlib import Path

def render(transcript_path: str) -> str:
    with open(transcript_path) as f:
        content = f.read()

    content = re.sub(r'^#{1,3} .*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'^---+\s*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'\[EMPHASIS\](.*?)\[/EMPHASIS\]', r'\1', content)
    content = re.sub(r'\[PAUSE\]', '...', content)
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    content = re.sub(r'`[^`]+`', lambda m: m.group(0).strip('`'), content)
    # Strip bold markdown speaker labels: **NOVA:** or **ALLOY:** → NOVA: or ALLOY:
    content = re.sub(r'^\*\*(NOVA|ALLOY):\*\*', r'\1:', content, flags=re.MULTILINE)
    # Also strip any remaining bold markdown
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
    content = re.sub(r'\*([^*]+)\*', r'\1', content)
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()

    paragraphs = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 20]

    def tag_paragraph(p):
        # Detect speaker from leading "ALLOY:" or "NOVA:" prefix, then strip it from spoken text
        if re.match(r'^ALLOY:', p):
            spoken = re.sub(r'^ALLOY:\s*', '', p)
            return f'[ALLOY]: {spoken}'
        elif re.match(r'^NOVA:', p):
            spoken = re.sub(r'^NOVA:\s*', '', p)
            return f'[NOVA]: {spoken}'
        else:
            return f'[NOVA]: {p}'

    nova_script = '\n\n'.join(tag_paragraph(p) for p in paragraphs)

    output_path = Path(transcript_path).parent / (Path(transcript_path).stem + '_nova.md')
    with open(output_path, 'w') as f:
        f.write(nova_script)

    print(f"✅ Rendered {len(paragraphs)} paragraphs → {output_path}")
    print(f"\nFirst 2 paragraphs (verify structure):")
    for p in paragraphs[:2]:
        print(f"  → {p[:120]}...")
    return str(output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('transcript', help='Path to episode transcript markdown')
    args = parser.parse_args()
    render(args.transcript)
