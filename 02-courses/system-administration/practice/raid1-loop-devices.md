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

RAID creation, filesystem formatting, mounting and cleanup have not been reported as completed. No storage changes were performed by the agent.

## Next step in the practice machine

Verify the mappings before writing metadata:

```sh
sudo losetup --list
lsblk -o NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS /dev/loop0 /dev/loop1
cat /proc/mdstat
```

Confirm both paths still refer to the intended disposable images, are not mounted or used by another array, and that `/dev/md0` is available. Loop numbers can change after detachment or restart.

Once verified, the adapted creation command is:

```sh
sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 /dev/loop0 /dev/loop1
```

This command writes RAID metadata to those members. `--level=1` selects mirroring; `--raid-devices=2` specifies two members. [mdadm reference](https://manpages.debian.org/testing/mdadm/mdadm.8.en.html).

Inspect actual results with:

```sh
cat /proc/mdstat
sudo mdadm --detail /dev/md0
```

`[UU]` indicates both expected members are present and active; it alone does not establish that initial synchronization has finished. Also inspect any recovery/resync progress and detailed state. `[U_]` or `[_U]` indicates a missing active member in a two-member array. [Linux MD reference](https://manpages.debian.org/testing/mdadm/md.4.en.html).

## Evidence to record

Record the actual creation outcome, array state, member count, synchronization progress and reported capacity. Add formatting and mounting results only after those steps are performed. A screenshot requested by the external exercise is not yet supplied.

## Capacity reasoning

A two-member mirror stores two copies, so its nominal capacity is about that of the smaller member, not their sum. Filesystem and RAID metadata reduce usable capacity. Two loop devices backed by the same physical disk demonstrate mirroring mechanics but do not protect against loss of that physical disk.

## Pending reflection

Explain what `--level=1` selects, why capacity is not doubled, and how member availability differs from completed synchronization. Record the student's answers and observations when available.
