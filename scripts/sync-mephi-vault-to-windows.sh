#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="${MEPHI_SYNC_SOURCE:-$ROOT/obsidian-mephi-vault}"
DEST="${MEPHI_SYNC_DEST:-/mnt/c/Users/Ерков Артемий Кирилл/Documents/obsidian-mephi-vault}"
STATE="${MEPHI_SYNC_STATE:-$ROOT/.local/vault-sync}"
mkdir -p "$STATE"
exec 9>"$STATE/sync.lock"
flock -n 9 || exit 0
[[ -f "$SRC/CLAUDE.md" && -f "$SRC/00-standards/documentation-standard.md" ]] || {
  echo 'Refusing sync: source vault is incomplete' >&2
  exit 1
}
[[ -d "$(dirname -- "$DEST")" ]] || {
  echo 'Windows Documents directory is unavailable' >&2
  exit 1
}
[[ "$(git -C "$SRC" branch --show-current)" == main ]] || exit 0
SRC="$(realpath -- "$SRC")"
DEST="$(realpath -m -- "$DEST")"
[[ "$DEST" != / && "$DEST" != "$SRC" && "$DEST/" != "$SRC/"* && "$SRC/" != "$DEST/"* ]] || {
  echo 'Refusing sync: source and destination overlap.' >&2
  exit 1
}
mkdir -p "$DEST"
# Preserve newer Windows edits, and back up any overwritten/deleted files.
changes=$(rsync -rtc --itemize-changes --update --delete-delay --backup \
  --backup-dir="$STATE/backups/$(date -u +%Y%m%dT%H%M%S.%N)" \
  --exclude '.git/' \
  --exclude '.obsidian/' \
  --exclude '.trash/' \
  --exclude '.env' --exclude '.env.*' \
  --exclude '*.pem' --exclude '*.key' \
  "$@" "$SRC/" "$DEST/")
# Color groups are shared. Other Obsidian settings remain local to Windows.
dry_run=false
for argument in "$@"; do
  case "$argument" in --dry-run|-n) dry_run=true ;; esac
done
if [[ "$dry_run" == false ]]; then
  python3 "$ROOT/obsidian-mephi-vault/scripts/sync-vault-graph.py" "$SRC" "$DEST" "$STATE"
fi
[[ -n "$changes" ]] || exit 0
printf '%s\n' "$changes"
printf '%s synced MEPHI vault to Windows\n' "$(date -Is)"
