#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
STARTUP='/mnt/c/Users/Ерков Артемий Кирилл/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup'
LAUNCHER="$ROOT/obsidian-mephi-vault/scripts/start-mephi-vault-sync.cmd"
TARGET="$STARTUP/start-mephi-vault-sync.cmd"
[[ -d "$STARTUP" ]] || { echo 'Windows Startup directory unavailable' >&2; exit 1; }
if [[ -e "$TARGET" ]] && ! cmp -s "$LAUNCHER" "$TARGET"; then
  echo 'An unrelated launcher already exists at the target; leaving it untouched' >&2
  exit 1
fi
UNIT="$HOME/.config/systemd/user/mephi-vault-sync.service"
if [[ -e "$UNIT" ]] && ! head -1 "$UNIT" | grep -Fq '# MEPHI vault synchronization.'; then
  echo 'An unrelated service unit exists. Installation stopped.' >&2
  exit 1
fi
mkdir -p "$ROOT/.local/vault-sync" "$(dirname -- "$UNIT")"
if [[ -e "$UNIT" ]]; then
  cp "$UNIT" "$ROOT/.local/vault-sync/service-$(date -u +%Y%m%dT%H%M%S).bak"
fi
systemctl --user stop mephi-vault-sync.service 2>/dev/null || true
cp "$ROOT/obsidian-mephi-vault/scripts/mephi-vault-sync.service" "$UNIT"
cp "$LAUNCHER" "$TARGET"
systemctl --user daemon-reload
systemctl --user enable --now mephi-vault-sync.service
bash "$ROOT/obsidian-mephi-vault/scripts/sync-mephi-vault-to-windows.sh"
DEST='/mnt/c/Users/Ерков Артемий Кирилл/Documents/obsidian-mephi-vault'
mkdir -p "$DEST/.obsidian"
if [[ ! -e "$DEST/.obsidian/app.json" ]]; then
  cp "$ROOT/obsidian-mephi-vault/.obsidian/app.json" "$DEST/.obsidian/app.json"
fi
printf 'Installed Windows sign-in launcher: %s\n' "$TARGET"
