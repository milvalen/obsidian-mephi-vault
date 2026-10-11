---
title: "Module 3 review: software delivery and storage"
type: review
status: draft
program: software-engineering
created: 2026-10-11
updated: 2026-10-11
course: System Administration
tags:
  - linux
  - packages
  - containers
  - storage
---
# Module 3 review: software delivery and storage

[System Administration](system-administration.md) · [RPM packages and digital signatures](rpm-and-digital-signatures.md)

## Course context

This summary covers owner-supplied material dated 2026-10-11 at 01:38. It groups Module 3 topics before the module's final test, identified in that material as Section 6. The supplied material links the RAID comparison to Section 3.5. The original course URL, complete section numbering and test questions are unknown. The vault does not store the original text. The student did not report a review attempt.

## Detailed topic notes

- [Software delivery, dependencies and archives](software-delivery.md)
- [APT and DNF package management](apt-and-dnf.md)
- [Container images, lifecycle and data](container-fundamentals.md)
- [Dockerfiles and build caching](dockerfile-and-build-cache.md)
- [Docker Compose services, readiness and persistence](docker-compose.md)
- [Image registries, tags and distribution](image-registries.md)
- [RAID layouts, capacity and Linux mdadm](raid-and-mdadm.md)
- [LVM allocation and filesystem growth](lvm-and-filesystem-growth.md)

The agent wrote these topic notes from this review and official references. The exact original lecture content remains unknown.

## Software delivery

Binary packages provide a prepared build that is usually quick to install. A source build permits custom changes. It requires build tools, dependencies, and more work. Neither delivery method alone shows that software is trustworthy.

A dependency is a required program, library or capability. Package managers use metadata to resolve dependencies, subject to available packages and compatible versions. Repositories provide indexes describing versions, dependencies and checksums. Signature verification depends on the system and configuration.

Archive creation and compression are separate operations. `tar` groups files into an archive. GNU tar can invoke a compressor such as gzip or xz. An uncompressed `.tar` and a compressed `.tar.gz` therefore differ. [GNU tar manual](https://www.gnu.org/software/tar/manual/html_node/gzip.html).

## APT and DNF

APT usually manages `.deb` packages on Debian and Ubuntu. DNF manages `.rpm` packages on distributions such as Fedora, Rocky Linux and AlmaLinux. Similar command names do not guarantee identical options or behavior.

| Task | APT | DNF |
| --- | --- | --- |
| Search | `apt search NAME` | `dnf search NAME` |
| Install | `apt install NAME` | `dnf install NAME` |
| Remove | `apt remove NAME` | `dnf remove NAME` |
| Inspect | `apt show NAME` | `dnf info NAME` |
| Refresh metadata | `apt update` | `dnf makecache --refresh` |
| Upgrade installed packages | `apt upgrade` | `dnf upgrade` |

`apt update` refreshes package indexes. It does not upgrade installed software. `apt upgrade` uses available indexes to upgrade installed packages, may add required dependencies, and does not remove existing packages. Removal does not always remove package configuration. [apt(8)](https://manpages.debian.org/testing/apt/apt.8.en.html).

Configure APT sources in `/etc/apt/sources.list` or files under `/etc/apt/sources.list.d/`. Sources can use the deb822 `.sources` format. [sources.list(5)](https://manpages.debian.org/testing/apt/sources.list.5.en.html). DNF usually reads `/etc/dnf/dnf.conf` and `.repo` files in `/etc/yum.repos.d/`. A new repository adds publishers and packages to the trusted set. [DNF configuration](https://dnf.readthedocs.io/en/latest/conf_ref.html).

## Images, containers and Dockerfiles

An image contains filesystem layers and execution metadata. A container is an instance created from an image. It can be running or stopped. Each container has its own writable layer above shared image layers. Volumes and bind mounts store data separately from that layer. [Docker storage drivers](https://docs.docker.com/engine/storage/drivers/).

Linux containers use the kernel of the environment running the Docker engine, with namespaces for isolation and cgroups for resource control. A virtual machine has a guest kernel. On Docker Desktop, Linux containers typically run inside a Linux VM rather than sharing a Windows or macOS kernel directly. [What is a container?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/).

`RUN` executes during image building. `COPY` and `ADD` introduce files into image layers.

`CMD` specifies the default runtime command or arguments. Its effect depends on `ENTRYPOINT`.

A runtime command can override it. It changes image configuration but does not run its command during the build. [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).

If dependencies permit it, put stable build steps before source files that change frequently. Changes can invalidate subsequent cached steps. Cache reuse depends on instructions and their inputs. Layers are not a guarantee of automatic reuse. [Build cache invalidation](https://docs.docker.com/build/cache/invalidation/).

## Compose and registries

Compose declares services, networks and volumes in YAML. `compose.yaml` is the preferred filename. `docker-compose.yml` remains supported. Use the current CLI form `docker compose`. [Compose file reference](https://docs.docker.com/reference/compose-file/).

Services on the same Compose network can resolve one another by service name. Connect with the service name and container port. Published host ports serve a different access path. [Compose networking](https://docs.docker.com/compose/how-tos/networking/).

Short-form `depends_on` shows dependency startup order, not application readiness. Long-form `depends_on` with `condition: service_healthy` waits for a dependency's configured health check. Applications still need to handle later failures and reconnect. [Startup order](https://docs.docker.com/compose/how-tos/startup-order/).

A registry distributes images. `docker tag` creates an image reference. `docker push` uploads it and `docker pull` downloads it. Tagging alone does not upload data.

A reference can include `HOST:PORT/NAMESPACE/IMAGE:TAG`. Without an explicit registry host, Docker uses Docker Hub. [Image tag reference](https://docs.docker.com/reference/cli/docker/image/tag/).

`localhost` refers to the loopback interface in the environment making the registry connection. A different machine cannot reach the first machine's registry using its own `localhost`. Use a reachable hostname or address. With a remote Docker engine, consider the engine's network context.

## RAID comparison

RAID combines devices for performance, availability or both. It does not replace backups: deletion, corruption and other failures can affect the entire array. The table assumes equal-sized disks and conventional layouts. `n` is the disk count and `S` is one disk's usable capacity. Figures exclude filesystem and metadata overhead.

| Level | Minimum disks in this layout | Failure tolerance | Usable capacity |
| --- | --- | --- | --- |
| RAID 0 | 2 | None. One failed member loses the array | `n × S` |
| RAID 1 | 2 | One failed disk in a two-disk mirror | `S`, or 50% for two disks |
| RAID 5 | 3 | Any one failed disk | `(n − 1) × S` |
| RAID 10 | 4 | One disk per mirror pair. Losing both in a pair loses the array | `(n / 2) × S`, or 50% |

RAID 0 stripes data, RAID 1 mirrors it, RAID 5 distributes parity, and conventional RAID 10 stripes across mirrored pairs. Linux MD can support other RAID 10 layouts. Four disks is the course's conventional layout assumption, not a universal implementation minimum.

[Linux MD reference](https://manpages.debian.org/testing/mdadm/md.4.en.html). `mdadm --create` creates Linux software arrays using a selected level and devices. The agent did not create an array. [Red Hat RAID guide](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/10/html/managing_storage_devices/managing-raid).

## LVM

LVM separates logical volume boundaries from individual device boundaries. Disks, partitions, or RAID devices can supply storage for physical volumes.

| Object | Role | Relevant commands |
| --- | --- | --- |
| Physical volume (PV) | Storage prepared for LVM | `pvcreate` |
| Volume group (VG) | Pool of storage extents from PVs | `vgcreate`, `vgextend` |
| Logical volume (LV) | Allocated virtual block device within a VG | `lvcreate`, `lvextend` |

LV growth requires available storage of the correct type. Block-device growth and filesystem growth are separate operations. `lvextend -r` requests both.

Online growth depends on filesystem support, mount state and available resize tools. Do not assume every filesystem or layout can grow while mounted. Growth and size reduction are different operations. The agent did not change disks or filesystems. [lvextend(8)](https://manpages.debian.org/testing/lvm2/lvextend.8.en.html).

## Bonus: RPM and signatures

An RPM contains a payload and metadata, optionally including installation or removal scripts. A spec file describes packaging stages used by `rpmbuild`. See [RPM packages and digital signatures](rpm-and-digital-signatures.md) for section meanings, GPG examples and the recorded one-byte-change check.

APT authenticates repository Release metadata and follows checksums through package indexes to `.deb` files. DNF can check signatures on RPM packages and separately on repository metadata. The two mechanisms are different. Key source information matters even when a signature is mathematically valid.

## Recall questions

1. What are the tradeoffs between binary packages and source builds?
2. How does archiving differ from compression?
3. Why does `apt update` not install available upgrades?
4. What trust decision accompanies adding a repository?
5. How do an image and a stopped container differ?
6. When do `RUN` and `CMD` take effect?
7. Why can ordinary `depends_on` leave an application waiting for its database?
8. Why does a registry reference using `localhost` fail on another machine?
9. For four equal 1 TB disks, what nominal capacity and failure tolerance do conventional RAID 0, 5 and 10 provide?
10. Why can two failed disks be survivable in one RAID 10 case and fatal in another?
11. How do PV, VG and LV relate, and what does `lvextend -r` request?
12. How do APT and DNF differ in signature verification?

## Verification limits

The agent read the official references above on 2026-10-11. This is an English summary with technical clarifications, not a transcript. The agent did not install packages, deploy Docker services, change storage, or execute a student test. Distribution and tool versions in the teaching environment are unknown, so the note remains a draft.
