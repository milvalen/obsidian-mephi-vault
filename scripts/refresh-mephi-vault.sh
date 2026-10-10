#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
SRC="${MEPHI_SYNC_SOURCE:-$ROOT/obsidian-mephi-vault}"
STATE="${MEPHI_SYNC_STATE:-$ROOT/.local/vault-sync}"
EXPECTED_ORIGIN="${MEPHI_SYNC_ORIGIN:-git@github.com:milvalen/obsidian-mephi-vault.git}"
mkdir -p "$STATE"
[[ "$(git -C "$SRC" remote get-url origin)" == "$EXPECTED_ORIGIN" ]] || {
  echo 'Remote refresh refused: origin does not match the MEPHI repository.' >&2
  exit 1
}
export GIT_TERMINAL_PROMPT=0
export GIT_SSH_COMMAND='ssh -F /dev/null -o BatchMode=yes -o ConnectTimeout=10 -o IdentitiesOnly=yes -i /home/eak/.ssh/id_ed25519_logopolza'
timeout 25 git -C "$SRC" fetch --quiet origin refs/heads/main:refs/remotes/origin/main
# Serialize checkout changes with the Windows copy. Fetch does not change source files.
exec 9>"$STATE/sync.lock"
flock -w 10 9 || exit 0
[[ "$(git -C "$SRC" branch --show-current)" == main ]] || exit 0
[[ -z "$(git -C "$SRC" status --porcelain --untracked-files=all)" ]] || exit 0
[[ ! -f "$(git -C "$SRC" rev-parse --path-format=absolute --git-path index.lock)" ]] || exit 0
if git -C "$SRC" merge-base --is-ancestor origin/main HEAD; then
  exit 0
fi
if ! git -C "$SRC" merge-base --is-ancestor HEAD origin/main; then
  echo 'Remote refresh skipped: local main and origin/main have diverged.' >&2
  exit 0
fi
git -C "$SRC" -c merge.autoStash=false -c core.hooksPath=/dev/null merge --ff-only --no-edit origin/main
