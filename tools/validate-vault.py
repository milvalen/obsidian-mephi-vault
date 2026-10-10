#!/usr/bin/env python3
"""Validate portable relative Markdown links and shared JSON settings."""
from pathlib import Path
import json
import re
from urllib.parse import unquote
root = Path(__file__).resolve().parents[1]
errors = []
for note in root.rglob('*.md'):
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', note.read_text()):
        target = target.split('#', 1)[0]
        if not target or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
            continue
        if not (note.parent / unquote(target)).exists():
            errors.append(f'{note.relative_to(root)}: missing {target}')
for settings in (root / '.obsidian').glob('*.json'):
    json.loads(settings.read_text())
if errors:
    raise SystemExit('\n'.join(errors))
print('Relative Markdown links and shared JSON settings passed.')
