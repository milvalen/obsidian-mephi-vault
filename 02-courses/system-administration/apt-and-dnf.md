---
title: "APT and DNF package management"
type: concept
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# APT and DNF package management

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

The agent wrote this study note from the Module 3 review that the owner supplied on 2026-10-11 at 01:38. Official documents give additional information. The exact course sections and software versions are unknown. The agent did not recover the original lecture or do the example procedures. The vault does not store the original text. The agent read the official references on 2026-10-11.

## Mental model

The package manager combines repository metadata with local package state to propose a transaction. Repository refresh, dependency resolution, download and installation are different stages. APT works with Debian packages. DNF works with RPM packages.

## Command reference

Replace `NAME` with a real package name. Installation, removal, and upgrades change the system. Examine the transaction before you accept it.

| Task | APT | DNF |
| --- | --- | --- |
| Search | `apt search NAME` | `dnf search NAME` |
| Inspect metadata | `apt show NAME` | `dnf info NAME` |
| Refresh indexes | `sudo apt update` | `sudo dnf makecache --refresh` |
| Install | `sudo apt install NAME` | `sudo dnf install NAME` |
| Remove | `sudo apt remove NAME` | `sudo dnf remove NAME` |
| Upgrade | `sudo apt upgrade` | `sudo dnf upgrade` |
| List installed packages | `apt list --installed` | `dnf list --installed` |

APT's `upgrade` can add dependencies but will not remove existing packages. `full-upgrade` can remove packages to complete an upgrade. `remove` usually leaves package configuration. `purge` removes configuration that the package manages. It does not remove all user files. `autoremove` targets dependencies no longer needed.

Prefer `apt-get`/`apt-cache` for scripts because `apt` targets interactive use. [APT manual](https://manpages.debian.org/testing/apt/apt.8.en.html).

DNF can refresh expired metadata during ordinary operations. `dnf repolist` lists enabled repositories. `dnf history` helps inspect transactions. DNF4 and DNF5 can differ in options and plugin commands. Check the installed version. [DNF command reference](https://dnf.readthedocs.io/en/latest/command_ref.html).

## Repository configuration and trust

APT reads `/etc/apt/sources.list` and files in `/etc/apt/sources.list.d/`. `.list` and deb822 `.sources` formats differ. [APT sources](https://manpages.debian.org/testing/apt/sources.list.5.en.html). DNF usually uses `/etc/dnf/dnf.conf` and `/etc/yum.repos.d/*.repo`. [DNF configuration](https://dnf.readthedocs.io/en/latest/conf_ref.html).

Before you add a repository, do these checks:

1. Identify the publisher.
2. Check the supported distribution and release.
3. Check the fingerprint of the signing key. Do not bypass checks to hide a trust failure. Read [RPM and digital signatures](rpm-and-digital-signatures.md) for the APT/DNF distinction.

## Worked reasoning and recall

A repository can publish a new version. The next `apt update` gets metadata about that version. A later installation transaction changes installed packages.

1. Why can a dependency conflict prevent installation?
2. What differs between `remove`, `purge` and `autoremove`?
3. Which command lists enabled DNF repositories?
