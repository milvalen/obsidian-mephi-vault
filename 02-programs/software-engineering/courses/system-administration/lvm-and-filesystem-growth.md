---
title: "LVM allocation and filesystem growth"
type: concept
status: draft
program: software-engineering
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# LVM allocation and filesystem growth

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

The agent wrote this study note from the Module 3 review that the owner supplied on 2026-10-11 at 01:38. Official documents give additional information. The exact course sections and software versions are unknown. The agent did not recover the original lecture or do the example procedures. The vault does not store the original text. The agent read the official references on 2026-10-11.

## Storage hierarchy

A physical volume (PV) is a device prepared for LVM. A volume group (VG) pools PV storage. A logical volume (LV) allocates extents from a VG and appears as a block device. Create a filesystem on that device. Mount the filesystem in a separate step.

LVM can use an underlying RAID device, but an ordinary linear LV does not automatically add redundancy. [LVM reference](https://manpages.debian.org/testing/lvm2/lvm.8.en.html).

A typical stack is `disks → RAID device → PV → VG → LV → filesystem → mount point`. RAID addresses layout and redundancy. LVM addresses allocation flexibility.

## Commands and inspection

| Action | Command family |
| --- | --- |
| Prepare a PV | `pvcreate` |
| Create or expand a VG | `vgcreate`, `vgextend` |
| Allocate or extend an LV | `lvcreate`, `lvextend` |
| Inspect allocation | `pvs`, `vgs`, `lvs` |
| Inspect mounted capacity | `df -h` |

Creation commands change storage metadata. Check actual devices, backups and the intended target before using them. The agent did not do storage operations for this note.

## Growth example

Suppose a conventional LV is 10 GiB and its VG has 8 GiB free. An increase of 5 GiB makes the LV 15 GiB. The VG then has approximately 3 GiB free. This calculation excludes extent rounding and overhead. Filesystem capacity changes only after filesystem growth.

Example command for that example LV:

```sh
sudo lvextend -L +5G -r /dev/study-vg/data
```

`+5G` adds capacity. `-L 15G` instead requests a total size. `-r` requests filesystem resizing as part of the operation.

Success requires correct free extents, a supported filesystem and resize tooling. Mounted growth support depends on the filesystem and environment. Shrinking is a separate procedure with different constraints. [lvextend manual](https://manpages.debian.org/testing/lvm2/lvextend.8.en.html).

## Diagnosis and recall

If the LV is larger but `df` shows no change, check the filesystem size. Then check that `df` shows the correct mount. If the VG has no free space, adding capacity elsewhere does not automatically make it part of that VG.

1. Why does extending a VG not automatically extend an LV?
2. What is the difference between LV size and filesystem size?
3. How do `-L +5G` and `-L 5G` differ?
4. Does an ordinary LV provide disk failure tolerance?
