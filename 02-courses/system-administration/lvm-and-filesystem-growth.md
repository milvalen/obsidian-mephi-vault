---
title: "LVM allocation and filesystem growth"
type: concept
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
---
# LVM allocation and filesystem growth

[System Administration](system-administration.md) · [Module 3 review](module-3-review.md)

Reconstructed study note based on the owner's Module 3 review supplied on 2026-10-11 at 01:38, supplemented by official documentation. This is not a recovered lecture transcript. Exact course section mapping and environment versions are unconfirmed. Examples are illustrative and have not been run; original source text is not stored. Official references were consulted on 2026-10-11.

## Storage hierarchy

A physical volume (PV) is a device prepared for LVM. A volume group (VG) pools PV storage. A logical volume (LV) allocates extents from a VG and appears as a block device. A filesystem is placed on that device and mounted separately. LVM can use an underlying RAID device, but an ordinary linear LV does not automatically add redundancy. [LVM reference](https://manpages.debian.org/testing/lvm2/lvm.8.en.html).

A typical stack is `disks → RAID device → PV → VG → LV → filesystem → mount point`. RAID addresses layout and redundancy; LVM addresses allocation flexibility.

## Commands and inspection

| Action | Command family |
| --- | --- |
| Prepare a PV | `pvcreate` |
| Create or expand a VG | `vgcreate`, `vgextend` |
| Allocate or extend an LV | `lvcreate`, `lvextend` |
| Inspect allocation | `pvs`, `vgs`, `lvs` |
| Inspect mounted capacity | `df -h` |

Creation commands change storage metadata. Check actual devices, backups and the intended target before using them. No storage operations were performed for this note.

## Growth example

Suppose a conventional LV is 10 GiB and its VG has 8 GiB free. Adding 5 GiB makes the LV 15 GiB and leaves approximately 3 GiB unallocated, ignoring extent rounding and overhead. Filesystem capacity changes only when its filesystem is grown.

Illustrative command for that hypothetical LV:

```sh
sudo lvextend -L +5G -r /dev/study-vg/data
```

`+5G` adds capacity; `-L 15G` instead requests a total size. `-r` requests filesystem resizing as part of the operation. Success requires appropriate free extents, a supported filesystem and resize tooling. Mounted growth support depends on the filesystem and environment. Shrinking is a separate procedure with different constraints. [lvextend manual](https://manpages.debian.org/testing/lvm2/lvextend.8.en.html).

## Diagnosis and recall

If an LV is larger but `df` is unchanged, inspect whether its filesystem was resized and whether the expected mount is being observed. If the VG has no free space, adding capacity elsewhere does not automatically make it part of that VG.

1. Why does extending a VG not automatically extend an LV?
2. What is the difference between LV size and filesystem size?
3. How do `-L +5G` and `-L 5G` differ?
4. Does an ordinary LV provide disk failure tolerance?
