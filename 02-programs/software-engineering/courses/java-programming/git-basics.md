---
title: Git basics and SSH keys for GitHub
type: lecture
status: draft
program: software-engineering
course: Java Programming
created: 2026-11-11
updated: 2026-11-11
---
# Git basics and SSH keys for GitHub

[Java Programming](java-programming.md) · [Java strings](strings.md) · [Home](../../../../README.md)

## Context and evidence

The owner supplied this unit text on 2026-11-11. The preceding unit made a GitHub account. The next unit is about branches.
Its module number, author, and URL are unknown. The text refers to two screencasts and several screenshots. The owner did not supply them.
The text asks for a project from earlier modules and uses an IDE. Thus this note is in the Java course. This placement is an assumption.
The vault keeps an English summary, not the original text or images.

The agent ran the Git commands below with Git 2.50.1 and OpenSSH 10.2p1 on macOS on 2026-11-11.
The test repository and test keys were in a temporary folder. The agent did not connect to GitHub.

Sources for agent checks:

- [Pro Git, section 1.3, "What is Git?"](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F)
- [GitHub: generating a new SSH key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [GitHub: testing your SSH connection](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)
- [GitHub: about remote repositories](https://docs.github.com/en/get-started/git-basics/about-remote-repositories)

## Skills for assessed work

The unit ends with a practice check. Its content is unknown. The unit teaches these skills:

1. Make a local repository and record the first commit.
2. Read `git status` and know the state of each file.
3. Connect the repository to GitHub and send commits with `git push`.
4. Make an SSH key, add it to GitHub, and test it.
5. Do the same operations in an IDE.

## Local repository

| Command | Result |
| --- | --- |
| `git init` | Makes the `.git` folder. Git does not record files yet |
| `git status` | Shows the state of each file |
| `git add file` | Puts the current version of one file in the staging area |
| `git add .` | Puts all changes in the current folder and its subfolders in the staging area |
| `git commit -m "message"` | Records the staging area as a new commit in the local history |

Before the first commit, set your name and email. Use the email of your GitHub account:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## Three areas and file states

| Area | Meaning |
| --- | --- |
| Git directory (`.git`) | The database of all commits. A clone copies it |
| Working directory | The files on the disk that you change |
| Staging area (index, `.git/index`) | The list of changes for the next commit |

| State | Meaning | `git status --short` |
| --- | --- | --- |
| Untracked | Git has no record of the file | `??` |
| Modified | The file is different from the last commit, and the change is not staged | ` M` |
| Staged | The change is in the staging area | `M ` |
| Committed | The change is in a commit in the local history | No line |

Agent check: a file changed again after `git add` shows `MM`. One version is staged, and a newer version is only in the working directory.
A commit then records the staged version only.

## Send commits to GitHub

A commit is local. `git push` sends commits to a remote repository. The unit does not show how to connect one:

```bash
git remote add origin git@github.com:USER/REPO.git
git push -u origin main
```

`-u` connects the local branch to the remote branch. After this, `git push` alone is sufficient.
Agent check: without a remote, `git push` gives `fatal: No configured push destination` and exit code 128.

Git 2.50.1 with no configuration names the first branch `master`. GitHub names it `main`.
Use the branch name that `git branch --show-current` gives.

## SSH key

An SSH key is a pair of keys:

- The public key, in the `.pub` file, goes to GitHub. Other persons can see it.
- The private key stays on your computer. Do not send it to anyone.

The client proves that it has the private key. The private key does not go to the server.

```bash
ls ~/.ssh
ssh-keygen -t ed25519 -C "you@example.com"
cat ~/.ssh/id_ed25519.pub
```

1. Copy the full line from the `.pub` file.
2. On GitHub, open Settings, SSH and GPG keys, New SSH key. Paste the line.
3. Test the connection with `ssh -T git@github.com`.

GitHub documents this success message: "Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access."
On the first connection, SSH asks to confirm the host fingerprint. Compare it with the fingerprints that GitHub publishes.

Agent check: `ssh-keygen -t ed25519 -f k -N ''` made the files `k` and `k.pub`. The public key line starts with `ssh-ed25519`. The text after `-C` is the third field of this line.

## Source corrections

| Source statement | Correction |
| --- | --- |
| After `git init`, Git tracks all changes | `git init` only makes the repository. Agent check: after `git init`, `git status` shows all files as `??` (untracked), and the index has 0 files |
| `git add .  // ...` and `git commit -m"..." // ...` | `//` is not a comment in a shell. Agent check: both lines fail with `fatal: '//' is outside repository` and exit code 128. In a shell, a comment starts with `#` |
| "Modified" is a change to a saved commit | A commit does not change. "Modified" is a file in the working directory that is different from the last commit and not staged |
| Three states only | A new file has a fourth state: untracked |
| No step to set the name and email | Agent check: with no configuration, Git made a commit with a name and email that it guessed from the system user and host name. GitHub cannot connect such an email to your account |
| No `git remote add` step | `git push` needs a remote. See "Send commits to GitHub" |
| `ssh-keygen -t rsa -b 4096` | GitHub recommends `-t ed25519`. It recommends RSA only for a legacy system. The default file is then `id_ed25519`, not `id_rsa` |
| Use the email of your GitHub account in `-C` | GitHub also gives this instruction. The text after `-C` is only a label. It has no effect on the check |
| Git asks for the key password | SSH asks for the passphrase of the key, not Git. On macOS, `ssh-add --apple-use-keychain` keeps it in the keychain |
| The test command is `ssh git@github.com` | GitHub documents `ssh -T git@github.com`. `-T` stops the request for a terminal |
| SSH is necessary to work without a password prompt | GitHub does not accept account passwords for Git over HTTPS. Use a personal access token or SSH |

## Common errors

| Symptom | Cause | Correction |
| --- | --- | --- |
| `nothing to commit` after a change | The change is not staged | `git add`, then `git commit` |
| `Permission denied (publickey)` | GitHub does not have this public key, or SSH does not use it | Add the `.pub` line on GitHub. Run `ssh-add` |
| Commits on GitHub show no avatar | `user.email` is not an email of the account | Set `git config --global user.email` |
| A file is missing from a commit after `git add .` | The command ran in a subfolder | Run `git add .` in the repository root, or `git add -A` |

## Recall questions

1. What does `git init` make? Does Git track the files after it?
2. What are the working directory, the staging area, and the Git directory?
3. What does `MM` in `git status --short` mean?
4. Which part of `git add .` sets the scope of the command?
5. Why must you set `user.email` before the first commit?
6. Which two commands connect a local repository to GitHub and send the first commit?
7. Which key goes to GitHub, and which key stays on the computer?
8. Which key type does GitHub recommend?
9. Which command tests the SSH connection, and what is the correct answer?
10. Why do copied lines with `//` fail in a shell?

## Open questions

- The module number, the author, and the URL of the unit.
- The content of the two screencasts and of the practice check.
- The IDE that the course uses.
