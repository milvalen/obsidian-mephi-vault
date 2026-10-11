# Windows vault synchronization

[Home](../README.md)

Main source: `/home/eak/mephi/obsidian-mephi-vault`.
Personal remote: `git@github.com:milvalen/obsidian-mephi-vault.git`, branch `main`.
Open `C:\Users\Ерков Артемий Кирилл\Documents\obsidian-mephi-vault` as a vault in Windows Obsidian.
Keep the actual Windows profile name unchanged.

## Copy and remote updates

This setup uses the existing Logopolza sync method.
The service copies local saved changes every 3 seconds while WSL operates.
A separate worker fetches remote changes every 60 seconds. The network request timeout is 25 seconds.
The worker permits only the configured personal remote.
It applies a fast-forward only when `main` has no local file changes.

It never commits, pushes, stashes, or resets files.

A network failure does not stop local copies.
Windows contains a one-way copy. Its changes do not return to Linux.
The service keeps newer Windows files. Correct differences manually in Linux.

The service makes backups before file replacement or deletion.
Backups are in `/home/eak/mephi/.local/vault-sync/backups`.
No automatic backup retention policy is configured.

## Device settings

The copy excludes `.git`, `.obsidian`, `.trash`, environment files, and private-key patterns.
A separate step copies only graph `colorGroups`.
Other Windows settings remain local.
At installation, the installer copies `app.json` only if the Windows file is absent.
You can enable core Templates with the folder `90-templates`.

## Startup and control

The persistent user service is `mephi-vault-sync.service`.
A Windows Startup launcher starts it through WSL `Ubuntu-24.04` as `eak`.
The [copy script](../scripts/sync-mephi-vault-to-windows.sh) is in this repository.
The installer refuses conflicting units or launchers.
The log is `/home/eak/mephi/.local/vault-sync/sync.log`.

```sh
bash scripts/install-mephi-vault-sync.sh
systemctl --user status mephi-vault-sync.service
systemctl --user stop mephi-vault-sync.service
python3 tools/test_vault_sync.py
```

A service stop does not remove startup enablement.
Windows sign-out/sign-in and Obsidian display checks require separate interactive tests.

## Verification — 2026-10-11

The agent published the repository under `milvalen` with default branch `main`.
The agent verified that the user service was enabled and active.
The Windows README and Linux README had the same bytes.
An uncommitted probe reached Windows automatically. Its removal also reached Windows.

Checks with disposable test data passed for remote updates, local changes, divergent history, branch checks, and offline copies.
They also passed for exclusions, newer Windows edits, backups, deletions, graph settings, and daemon shutdown.
Shell syntax, systemd unit validation, relative links, and shared JSON checks passed.
The agent did not test Windows sign-in or the Obsidian display.
These statements keep their actual verification date. The language review is not a new runtime check.
