---
title: RPM packages and digital signatures
type: lecture
status: draft
created: 2026-10-11
updated: 2026-10-11
course: System Administration
tags:
  - linux
  - packages
  - signatures
---
# RPM packages and digital signatures

[System Administration](system-administration.md) · [Sources](../../05-sources/sources.md)

## Course context

The owner supplied this material on 2026-10-11 at 01:33. It describes an ungraded demonstration: understanding RPM internals is not required to pass the course. These are reported course rules, not independently verified requirements. The block number is unknown. Referenced sections 1.5 and 3.1–3.4 have not been supplied. Original text is not retained.

## RPM contents

An RPM contains a file payload and metadata: name, version, dependencies, file information and checksums. Installation and removal scripts can include `%pre`, `%post`, `%preun` and `%postun`. These differ from spec build scripts. Dependencies can express capabilities and version constraints; they do not always require a separate package installed beforehand. Metadata supports transaction checks before package files are placed. [RPM documentation](https://rpm.org/docs/4.20.x/manual/spec.html).

## Spec files and package building

A spec file describes sources, metadata and package preparation. Header fields include `Name`, `Version`, `Release`, `Source` and `BuildRequires`.

| Section | Purpose |
| --- | --- |
| `%description` | Package description |
| `%prep` | Prepare sources and patches |
| `%build` | Compile or otherwise build the project |
| `%install` | Stage output in the temporary `buildroot` tree |
| `%check` | Run project checks when defined |
| `%files` | Select files for packaging |
| `%changelog` | Record package changes |

`%install` prepares package contents in `buildroot`; it does not install a finished RPM into the running system. `%description`, `%files` and `%changelog` contain data rather than executable build scripts. The stages executed depend on the `rpmbuild` mode. [Spec reference](https://rpm.org/docs/4.20.x/manual/spec.html).

## Signatures and key trust

A private key creates a signature, and the corresponding public key verifies it. A checksum detects changes but does not establish origin by itself: both the file and a checksum from an untrusted source can be replaced.

`Good signature` confirms that the signature matches the data and the identified key. Establishing the expected publisher also requires checking the key's provenance and fingerprint through a trusted channel. A name or email inside a key is insufficient. A distribution maintainer can be the signer rather than the upstream software author. [GnuPG guidance](https://gnupg.org/download/integrity_check.html).

A valid signature does not establish that software is harmless. Compromise of the trusted key or publisher remains a separate threat. [apt-secure](https://manpages.debian.org/testing/apt/apt-secure.8.en.html) explains this trust distinction.

## Detached GPG signature example

These commands sign an archive, not an RPM's embedded signature. Signing requires an available private key; verification requires the signer's public key.

```sh
gpg --detach-sign --armor package.tar.gz
gpg --verify package.tar.gz.asc package.tar.gz
```

The first command creates an ASCII-armored detached signature, `package.tar.gz.asc`, without changing the archive. Changing signed bytes invalidates the existing signature. [GPG reference](https://www.gnupg.org/documentation/manuals/gnupg24/gpg.1.html).

Verification on 2026-10-11 used an isolated temporary directory and a disposable Ed25519 key. The original `example.txt` returned `GOODSIG` and exit code 0. Replacing one ASCII byte produced `BADSIG` and a nonzero exit code. Personal keys and GPG configuration were not used. This was an agent check with synthetic data, not a completed student lab. RPM building and repository configuration were not tested.

## APT and DNF verification

| System | Signature checks | Link to the package file |
| --- | --- | --- |
| APT | Signed `InRelease`, or `Release` with detached `Release.gpg` | Release checksums authenticate Packages indexes; those indexes contain `.deb` checksums |
| DNF | `gpgcheck` checks RPM package signatures; `repo_gpgcheck` separately controls repository metadata verification | Metadata verification complements package signature verification |

APT uses the chain: signed Release → Packages index checksum → package checksum. `apt-secure` does not separately verify a signature on each `.deb`. [apt-secure](https://manpages.debian.org/testing/apt/apt-secure.8.en.html).

DNF controls package signatures and metadata signatures separately. Effective behavior depends on configuration and RPM policy; package checking does not automatically enable metadata signature checking. [DNF configuration reference](https://dnf.readthedocs.io/en/latest/conf_ref.html).

## Common misunderstandings

- Automatic verification does not require the administrator to run a separate manual check each time.
- APT and DNF do not use identical signature verification schemes.
- A valid signature still requires establishing trust in the signing key.
- `%install` operates on the build tree, and not every spec section is executable.

## Recall questions

1. Why does a checksum from the same untrusted source not authenticate the publisher?
2. How does a valid signature differ from a verified signer identity?
3. Where are files placed during `%install`?
4. How does `%post` differ from `%build`?
5. How does APT connect a Release signature to a specific `.deb`?
6. How do DNF's `gpgcheck` and `repo_gpgcheck` differ?
7. What happens if one byte changes after signing?

## References and verification limits

Provenance: owner-supplied material dated 2026-10-11 at 01:33. The original text is not stored. Official RPM 4.20, GnuPG, APT and DNF references are linked beside claims and were consulted on 2026-10-11. The teaching environment's distribution and versions are unknown. This note remains a draft because course context and syllabus alignment are unconfirmed. The recorded GPG check retains its actual verification date; translation does not constitute a new runtime check.
