#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE="${MEPHI_SYNC_STATE:-$ROOT/.local/vault-sync}"
SCRIPT="$ROOT/obsidian-mephi-vault/scripts/start-mephi-vault-sync.sh"
mkdir -p "$STATE"
if [[ "${1:-}" == '--run' ]]; then
  exec 8>"$STATE/daemon.lock"
  flock -n 8 || exit 0
  echo "$$" > "$STATE/daemon.pid"
  remote_pid=''
  sleep_pid=''
  cleanup() {
    trap - EXIT TERM INT
    [[ -z "$remote_pid" ]] || kill "$remote_pid" 2>/dev/null || true
    [[ -z "$sleep_pid" ]] || kill "$sleep_pid" 2>/dev/null || true
    wait 2>/dev/null || true
    rm -f "$STATE/daemon.pid"
  }
  trap cleanup EXIT
  trap 'exit 0' TERM INT
  next_refresh=0
  while true; do
    if (( SECONDS >= next_refresh )); then
      if [[ -z "$remote_pid" ]] || ! kill -0 "$remote_pid" 2>/dev/null; then
        [[ -z "$remote_pid" ]] || wait "$remote_pid" || true
        bash "$ROOT/obsidian-mephi-vault/scripts/refresh-mephi-vault.sh" &
        remote_pid=$!
      fi
      next_refresh=$((SECONDS + 60))
    fi
    bash "$ROOT/obsidian-mephi-vault/scripts/sync-mephi-vault-to-windows.sh" || \
      printf '%s Windows copy failed; the next cycle will retry.\n' "$(date -Is)"
    sleep 3 &
    sleep_pid=$!
    wait "$sleep_pid"
  done
else
  if systemctl --user is-active --quiet mephi-vault-sync.service; then
    echo 'MEPHI vault sync service is already active'
    exit 0
  fi
  if [[ -f "$HOME/.config/systemd/user/mephi-vault-sync.service" ]]; then
    systemctl --user start mephi-vault-sync.service
    exit 0
  fi
  systemd-run --user --collect --unit=mephi-vault-sync \
    --property=Restart=on-failure --property=RestartSec=10 \
    --property="StandardOutput=append:$STATE/sync.log" \
    --property="StandardError=append:$STATE/sync.log" \
    /bin/bash "$SCRIPT" --run
  printf 'MEPHI sync service started; log: %s/sync.log\n' "$STATE"
fi
