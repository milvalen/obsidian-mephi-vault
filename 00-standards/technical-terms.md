# Technical terms

[Study note standard](documentation-standard.md) · [Home](../README.md)

These terms name computing concepts used in this vault.
They are subject-field terms, not additions to the official STE dictionary.
Use the noun and verb forms only with the meanings specified here.
Add every new technical term in the same change that first uses it. Define its meaning and permitted form. Do not use a new term to hide unclear prose.

## Study and evidence terms

| Term | Meaning |
| --- | --- |
| vault | The collection of Obsidian study notes |
| source reference | Data that identifies a source without a copy of its text |
| draft | A note with facts or course details that need a check |
| checked | A note supported by the stated source or calculation checks |
| example | A proposed case or procedure, without an execution claim |
| owner-reported observation | A result that the owner supplied |
| agent check | A check that the agent actually executed |
| recall question | A question to answer from memory before a source check |

## Computing nouns

| Term | Meaning |
| --- | --- |
| binary package | Prepared software and package-manager metadata |
| repository | A package source or an image store, as identified by context |
| dependency | A required program, library, or capability |
| metadata | Data that describes a resource or its contents |
| image | Immutable container content and runtime configuration |
| container | An instance of a container image |
| writable layer | Container-specific filesystem changes |
| volume | A Docker data store or an LVM storage object, as identified by context |
| registry | A service that stores and distributes container images |
| tag | A readable image reference that can change |
| digest | A content identifier calculated from a hash |
| loop device | A block device backed by a file |
| RAID array | A block device formed from multiple member devices |
| physical volume (PV) | A storage device prepared for LVM |
| volume group (VG) | A pool of LVM storage extents |
| logical volume (LV) | An LVM block device allocated from a VG |
| filesystem | The structure used to store and find files on storage |
| namespace | An isolated view of a class of Linux resources |
| listener | A socket that accepts incoming connections |
| loopback address | An address for the local network context |
| wildcard bind address | An address value that selects all local addresses in its address family |
| reverse proxy | A server that accepts requests and passes them to an upstream |
| upstream | An application or server to which a proxy sends requests |
| certificate | A signed document that binds an identity to a public key |
| unit | A systemd object that describes a service or another managed resource |
| journal | Structured log records stored by journald |
| log entry | One recorded event or request |
| metric | A measured value used to describe system or service state |
| WAF | A web application firewall that inspects HTTP transactions |
| anomaly score | A total from detection rules used for a policy decision |
| threshold | A value at which a configured decision applies |

## Computing verbs

| Verb | Technical action |
| --- | --- |
| authenticate | Check the identity claimed by a participant |
| bind | Assign a local address and port to a socket |
| execute | Carry out a computer command or instruction |
| verify | Check a digital signature or a specified computing constraint |
| run | Start or operate a program |
| compile | Convert source code into executable code |
| decrypt / encrypt | Convert between readable and protected data with a cryptographic key |
| format | Create a filesystem structure on a device |
| mount / unmount | Attach or detach a filesystem at a mount point |
| reload | Read and apply configuration without a full service stop |
| resolve | Obtain an address or another DNS record from a name |
| resize | Change the size of a storage object or filesystem |
| sign | Create a digital signature with a private key |
| synchronize | Make replicas consistent |
| validate | Check specified syntax, constraints, or identity rules |

Keep case-sensitive identifiers as written in commands and output.
Do not change names such as `proxy_pass`, `colorGroups`, or `Restart=on-failure` to match prose rules.
Official interface labels and code punctuation remain exact.
The Windows profile path contains Cyrillic characters. Keep that actual path unchanged.
