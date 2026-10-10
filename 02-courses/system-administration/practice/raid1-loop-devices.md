---
title: "Practice: RAID 1 with loop devices"
type: lab
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# Practice: RAID 1 with loop devices

[System Administration](../system-administration.md) · [RAID concepts](../raid-and-mdadm.md)

## Exercise reference

Chuck Nelson, [Introduction to Software RAID](https://chnelson.quarto.pub/citc1321/modules/06_Storage/Exercise_6.3.html), published 2025-10-22, consulted 2026-10-11. The exercise builds, formats and mounts a two-member RAID 1 array, then deactivates it. Its stated environment is Fedora 42. This external exercise's numbering does not establish a MEPHI course section number. Original page text is not retained.

## Progress and device record

The owner reports that two virtual disks are already attached:

| Member | Reported device path | Backing file | Size |
| --- | --- | --- | --- |
| First | `/dev/loop0` | Not supplied | Not supplied |
| Second | `/dev/loop1` | Not supplied | Not supplied |

Attachment is owner-reported, not independently verified in the practice machine. The agent's current WSL environment showed neither loop device in `lsblk` or `losetup --list` on 2026-10-11. That observation does not invalidate the report from a separate VM.

The owner supplied the output of `sudo mdadm --detail /dev/md0`. It confirms that the array exists with two active synchronized members. Formatting, mounting and cleanup remain unreported. No storage changes were performed by the agent.

## Reported array inspection

Source: owner-supplied command output from `milvalen@fedora`, received on 2026-10-11. Observed fields are summarized below; the terminal transcript is not stored. The array was not inspected directly by the agent.

| Field | Reported value |
| --- | --- |
| Array device | `/dev/md0` |
| Metadata version | `1.2` |
| RAID level | `raid1` |
| Creation time | `2026-10-11 02:12:16` |
| Last update time | `2026-10-11 02:14:23` |
| Array size | `510976 KiB`, displayed as `499.00 MiB` / `523.24 MB` |
| Used size per member | `510976 KiB`, displayed as `499.00 MiB` / `523.24 MB` |
| Configured / total devices | `2 / 2` |
| Array state | `clean` |
| Active / working devices | `2 / 2` |
| Failed / spare devices | `0 / 0` |
| Consistency policy | `resync` |
| Metadata persistence | Persistent superblock |
| Array name | `fedora:0` |
| Array UUID | `54812b0d:efa4e112:635092ef:436cbcbb` |
| Event count | `17` |

The output does not specify the timezone of its timestamps.

| RAID member slot | Device | Major:minor | Reported state |
| --- | --- | --- | --- |
| 0 | `/dev/loop0` | `7:0` | `active sync` |
| 1 | `/dev/loop1` | `7:1` | `active sync` |

The reported state and counts show a clean, non-degraded mirror at inspection time. `Consistency Policy: resync` names the policy, not an indication that synchronization is currently running. These results do not establish filesystem creation, mount status, a completed file-write test or protection against failure of the backing physical disk. [mdadm reference](https://manpages.debian.org/testing/mdadm/mdadm.8.en.html).

## Next step: filesystem preparation

First inspect the array in the practice VM:

```sh
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS /dev/md0
```

If this is the newly created disposable array, has no filesystem to retain, and is not mounted, the exercise's next operation is:

```sh
sudo mkfs.ext4 /dev/md0
```

Formatting creates a filesystem and overwrites existing filesystem data. Target the array device, not either member. Do not recreate the RAID array: it already exists. Record formatting output before proceeding to mount it.

A screenshot requested by the external exercise has not been supplied. Future observations must retain their actual timestamps; the array inspection above is not evidence of later steps.

## Capacity reasoning

The reported array and used-member sizes are equal: `510976 × 1024 = 523239424` bytes, or `499 MiB` (approximately `523.24 MB`). A two-member mirror stores two copies, so its nominal capacity is about that of the smaller member, not their sum. The complete loop-device sizes are still unknown. Filesystem and RAID metadata reduce usable capacity. Two loop devices backed by the same physical disk demonstrate mirroring mechanics but do not protect against loss of that physical disk.

## Pending reflection

Explain what `--level=1` selects, why capacity is not doubled, and how member availability differs from completed synchronization. Record the student's answers and observations when available.
