---
title: "Software delivery, dependencies and archives"
type: concept
status: draft
program: software-engineering
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Software delivery, dependencies and archives

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

The agent wrote this study note from the Module 3 review that the owner supplied on 2026-10-11 at 01:38. Official documents give additional information. The exact course sections and software versions are unknown. The agent did not recover the original lecture or do the example procedures. The vault does not store the original text. The agent read the official references on 2026-10-11.

## Delivery choices

A binary package contains a prepared build plus metadata for its package manager. A source archive contains source files. It does not automatically supply an installed program or package metadata. A container image packages userspace files and runtime configuration for a container engine. These choices differ in update ownership, compatibility and deployment workflow.

For a binary package, use this procedure:

1. Identify the distribution and architecture.
2. Select a trusted repository.
3. Examine the dependencies.
4. Examine the proposed installation transaction.

For a source build, use this procedure:

1. Get the source release specified by the project.
2. Verify the source.
3. Install the build dependencies.
4. Obey the project's build instructions.
5. Select a method to record installed files.
6. Select a method to remove those files. There is no universal build command for every project. Packaging the result can make later maintenance easier.

## Dependencies and repositories

Dependencies describe required libraries, programs or capabilities, sometimes with version constraints. Resolution finds a compatible transaction using available metadata. Unavailable or conflicting requirements can make it fail. Repositories provide indexed package metadata rather than only a folder of downloads. Continue with [APT and DNF](apt-and-dnf.md) and [package signatures](rpm-and-digital-signatures.md).

## Archiving versus compression

`tar` groups files. Compression reduces their encoded size. GNU tar can call gzip or xz. These example commands create an archive from an existing `notes/` directory and list its contents:

```sh
tar -cf notes.tar notes/
tar -czf notes.tar.gz notes/
tar -tf notes.tar
tar -tzf notes.tar.gz
```

`-c` creates, `-t` lists, `-f` names the archive, and `-z` uses gzip. Inspect an unfamiliar archive before extracting into a chosen directory. [GNU tar manual](https://www.gnu.org/software/tar/manual/html_node/gzip.html).

## Common mistakes and recall

An archive does not supply the same dependency and removal data as a package. For a source installation, make an upgrade plan. Do not assume that the distribution will maintain the build.

1. Which delivery method records distribution-managed dependencies?
2. What extra maintenance work follows a source installation?
3. Does changing `.tar` to `.tar.gz` compress a file? Explain.

Reference access limit: The request for the GNU tar manual page timed out on 2026-10-11. The note keeps the official reference link. The agent could not verify page access during this review.
