---
title: "RAID layouts, capacity and Linux mdadm"
type: concept
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# RAID layouts, capacity and Linux mdadm

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

Reconstructed study note based on the owner's Module 3 review supplied on 2026-10-11 at 01:38, supplemented by official documentation. This is not a recovered lecture transcript. Exact course section mapping and environment versions are unconfirmed. Examples are illustrative and have not been run; original source text is not stored. Official references were consulted on 2026-10-11.

## Layouts and failure domains

Use [the Module 3 RAID table](module-3-review.md#raid-comparison) for minimum disks and formulas under conventional equal-disk assumptions. Striping spreads data; mirroring keeps copies; parity permits reconstruction after the supported number of failures. RAID protects availability against certain device failures, not deleted files, malicious changes or every form of corruption.

For conventional four-disk RAID 10 with mirror pairs A/B and C/D, losing A and C leaves one copy in each pair. Losing A and B removes both copies in one pair. Two failures are therefore not always survivable. Linux MD supports additional layouts, so evaluate actual replica placement. [Linux MD](https://manpages.debian.org/testing/mdadm/md.4.en.html).

## Worked capacity example

For four equal 1 TB disks, ignoring overhead:

| Layout | Calculation | Nominal usable capacity |
| --- | --- | --- |
| RAID 0 | `4 × 1 TB` | 4 TB |
| RAID 1 across all four | One mirrored copy set | 1 TB |
| RAID 5 | `(4 − 1) × 1 TB` | 3 TB |
| Conventional RAID 10 | `(4 / 2) × 1 TB` | 2 TB |

The review's 50% RAID 1 figure applies to two disks; a four-way mirror uses 25% here. This is a synthetic calculation, not measured storage capacity.

## Array lifecycle

The conceptual sequence is: identify disposable members, choose a layout, create the MD device, monitor initialization, then place a filesystem or [LVM](lvm-and-filesystem-growth.md) above it. Creating an array writes member metadata; do not substitute live disks into a study example.

Command shape, deliberately not executable as written:

```text
mdadm --create MD_DEVICE --level=LEVEL --raid-devices=COUNT MEMBER_DEVICES...
```

Inspection examples include `cat /proc/mdstat` and `sudo mdadm --detail /dev/md0` when that array exists. Reassembling a known array is different from creating a new one. A degraded array needs monitoring and replacement; rebuilds do not restore independent backups. [mdadm manual](https://manpages.debian.org/testing/mdadm/mdadm.8.en.html).

## Recall

1. Why does RAID 0 have no failed-disk tolerance?
2. Which two failures destroy the example RAID 10?
3. Why is four-way RAID 1 not 50% efficient?
4. What remains unprotected when deleted data is mirrored?
