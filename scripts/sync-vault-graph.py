#!/usr/bin/env python3
"""Copy shared graph colors without replacing personal Obsidian settings."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime, timezone


def main():
    source, destination, state = map(Path, sys.argv[1:])
    source = source / '.obsidian/graph.json'
    destination = destination / '.obsidian/graph.json'
    if not source.is_file():
        return
    shared = json.loads(source.read_text())
    groups = shared.get('colorGroups')
    if not isinstance(groups, list):
        raise ValueError('Source graph colorGroups must be a list.')
    current = json.loads(destination.read_text()) if destination.exists() else {}
    if not isinstance(current, dict):
        raise ValueError('Destination graph settings must be an object.')
    if current.get('colorGroups') == groups:
        return
    if destination.exists():
        backup = state / 'backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ-graph')
        backup.mkdir(parents=True, exist_ok=True)
        shutil.copy2(destination, backup / 'graph.json')
    current['colorGroups'] = groups
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', dir=destination.parent, delete=False) as output:
            temporary = Path(output.name)
            output.write(json.dumps(current, indent=2) + '\n')
        temporary.replace(destination)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print('Synced shared Obsidian graph color groups.')


if __name__ == '__main__':
    main()
