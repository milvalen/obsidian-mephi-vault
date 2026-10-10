# Windows vault synchronization

[Home](../README.md)

Canonical source: `/home/eak/mephi/obsidian-mephi-vault`.
Personal remote: `git@github.com:milvalen/obsidian-mephi-vault.git`, branch `main`.
Open `C:\Users\Ерков Артемий Кирилл\Documents\obsidian-mephi-vault` as a vault in Windows Obsidian.

This adapts the existing Logopolza mechanism. Local saves copy every 3 seconds while WSL runs. A separate worker fetches every 60 seconds with a 25-second timeout. It permits only the configured personal remote, and applies a fast-forward only on clean `main`. It never commits, pushes, stashes or resets. Network failure does not stop local copies.

Windows is a one-way mirror. Newer Windows files are preserved but never copied back; reconcile edits manually in Linux. Replaced or deleted files are backed up under `/home/eak/mephi/.local/vault-sync/backups`. Deletions in Linux propagate to Windows with backups. There is no automatic backup retention policy.

The copy excludes `.git`, `.obsidian`, `.trash`, environment files and private-key patterns. Only graph `colorGroups` are copied separately; other Windows settings remain local. Initial `app.json` preferences are copied once at installation if absent. Core Templates can be enabled manually with folder `90-templates`.

The persistent user service is `mephi-vault-sync.service`. A Windows Startup launcher starts it through WSL `Ubuntu-24.04` as `eak`. Source scripts are in [scripts](../scripts/sync-mephi-vault-to-windows.sh); the installer refuses conflicting units or launchers. Logs are at `/home/eak/mephi/.local/vault-sync/sync.log`.

```sh
bash scripts/install-mephi-vault-sync.sh
systemctl --user status mephi-vault-sync.service
systemctl --user stop mephi-vault-sync.service
python3 tools/test_vault_sync.py
```

Stopping the service does not remove its enabled startup configuration. Windows sign-out/sign-in and Obsidian visual rendering require a separate interactive check.

## Verification — 2026-10-11

The repository was published under `milvalen` with default branch `main`. The user service was verified enabled and running, and the installed Windows README matched the Linux bytes. An uncommitted probe reached Windows automatically; its removal propagated automatically. Disposable regression checks passed for remote updates, dirty worktrees, divergence, branch guards, offline copying, exclusions, newer Windows edits, backups, deletions, graph settings and daemon shutdown. Shell syntax, systemd unit validation, relative note links and shared JSON settings passed. Windows sign-in and visual rendering in Obsidian were not exercised.
