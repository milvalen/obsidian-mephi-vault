---
title: "Software delivery, dependencies and archives"
type: concept
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Software delivery, dependencies and archives

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

Reconstructed study note based on the owner's Module 3 review supplied on 2026-10-11 at 01:38, supplemented by official documentation. This is not a recovered lecture transcript. Exact course section mapping and environment versions are unconfirmed. Examples are illustrative and have not been run; original source text is not stored. Official references were consulted on 2026-10-11.

## Delivery choices

A binary package contains a prepared build plus metadata for its package manager. A source archive contains source files; it does not automatically supply an installed program or package metadata. A container image packages userspace files and runtime configuration for a container engine. These choices differ in update ownership, compatibility and deployment workflow.

For a binary package, identify the distribution and architecture, select a trusted repository, inspect dependencies, then review the proposed installation transaction. For a source build, obtain the project's documented source release, verify it, install build dependencies, follow its own build instructions, and decide how to track and remove installed files. There is no universal build command for every project. Packaging the result can make later maintenance easier.

## Dependencies and repositories

Dependencies describe required libraries, programs or capabilities, sometimes with version constraints. Resolution finds a compatible transaction using available metadata; unavailable or conflicting requirements can make it fail. Repositories provide indexed package metadata rather than only a folder of downloads. Continue with [APT and DNF](apt-and-dnf.md) and [package signatures](rpm-and-digital-signatures.md).

## Archiving versus compression

`tar` groups files; compression reduces their encoded size. GNU tar can call gzip or xz. These illustrative commands create an archive from an existing `notes/` directory and list its contents:

```sh
tar -cf notes.tar notes/
tar -czf notes.tar.gz notes/
tar -tf notes.tar
tar -tzf notes.tar.gz
```

`-c` creates, `-t` lists, `-f` names the archive, and `-z` uses gzip. Inspect an unfamiliar archive before extracting into a chosen directory. [GNU tar manual](https://www.gnu.org/software/tar/manual/html_node/gzip.html).

## Common mistakes and recall

Confusing an archive with an installable package loses dependency and lifecycle information. Installing from source also means planning future upgrades rather than assuming the distribution will maintain that build.

1. Which delivery method records distribution-managed dependencies?
2. What extra maintenance work follows a source installation?
3. Does changing `.tar` to `.tar.gz` compress a file? Explain.

Reference access limit: direct retrieval of the GNU tar manual page timed out on 2026-10-11. The link is retained as the official reference; its availability was not verified during this reconstruction.
