---
title: Git branches
type: lecture
status: draft
program: software-engineering
course: Java Programming
created: 2026-11-11
updated: 2026-11-11
---
# Git branches

[Java Programming](java-programming.md) · [Git basics](git-basics.md) · [Merge conflicts](git-merge-conflicts.md) · [Home](../../../../README.md)

## Context and evidence

The owner supplied this unit text on 2026-11-11. It follows the [Git basics unit](git-basics.md). The [next unit](git-merge-conflicts.md) is about merge conflicts.
Its module number, author, and URL are unknown. The text refers to a diagram and two screencasts, one for the console and one for an IDE. The owner did not supply them.
The vault keeps an English summary, not the original text or images.

The agent ran the commands below with Git 2.50.1 on macOS on 2026-11-11, in a temporary repository with no Git configuration.

Sources for agent checks:

- [Pro Git, section 3.1, "Branches in a Nutshell"](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell)
- [`git branch` documentation](https://git-scm.com/docs/git-branch)
- [`git switch` documentation](https://git-scm.com/docs/git-switch)

## Skills for assessed work

1. Make a branch and move to it.
2. Move between branches, and know what happens to changes that are not committed.
3. Rename and delete a branch.
4. Do the same operations in an IDE.

## What a branch is

A branch is a name that points to one commit. A new commit moves the name of the current branch to this commit.
`HEAD` shows the current branch.

A new branch does not copy commits. The new branch and the old branch share all commits before the point where they separate.
Agent check: after one commit on `feature`, `git merge-base master feature` gives the last commit of `master`. Both branches use this commit.

Use a branch for work that can fail, for example a new function. The main branch stays unchanged until you join the work. The next unit describes this.

## Commands

| Purpose | Command in the source | Newer command | Note |
| --- | --- | --- | --- |
| Make a branch and move to it | `git checkout -b name` | `git switch -c name` | The branch starts at the current commit |
| Make a branch only | `git branch name` | | You stay on the current branch |
| Move to a branch | `git checkout name` | `git switch name` | Git changes the files in the working directory |
| Show branches | `git branch` | | `*` marks the current branch |
| Rename the current branch | `git branch -m new` | | |
| Rename a different branch | `git branch -m old new` | | You do not have to move to it |
| Delete a merged branch | `git branch -d name` | | Git refuses an unmerged branch |
| Delete an unmerged branch | `git branch -D name` | | The commits of the branch become difficult to find |

`git switch` has only branch operations. `git checkout` also restores files, so an error in its argument can remove changes.

## Changes that are not committed

A change that is not committed is not in a branch. It stays in the working directory when you move to a different branch.

| Case | Agent check |
| --- | --- |
| `git checkout -b feature` with a changed file | The change moves to `feature`. `git status` shows ` M f.txt` |
| `git checkout master` with the same change | The change moves back to `master` |
| A change that is different from the file in the target branch | Git refuses: `Your local changes to the following files would be overwritten by checkout`. Exit code 1 |

Before you move between branches, commit the change. Or keep it with `git stash`.

## Source corrections

| Source statement | Correction |
| --- | --- |
| Git makes the first branch at `git init` | Git selects only the name. Agent check: after `git init`, `git branch` shows no branches. The branch appears with the first commit |
| `master` or `main`: the name has no effect | Correct for Git. Git 2.50.1 with no configuration uses `master`. GitHub uses `main`. `git init -b main` or `init.defaultBranch` selects the name |
| The new branch takes the commits of the old branch | It does not copy commits. Both names point to shared commits |
| All changes in the new branch stay only in this branch | Only committed changes. A change that is not committed moves with you to the next branch |
| You must move to a branch before `git branch -m` | Only for the one-argument form. `git branch -m old new` renames a branch from a different branch |
| `git branch -d` needs only a different current branch | It also needs a merged branch. Agent check: an unmerged branch gives `the branch 'feat2' is not fully merged` and exit code 1. `-D` deletes it |
| Delete the current branch | Agent check: Git refuses with `cannot delete branch ... used by worktree` |

## Common errors

| Symptom | Cause | Correction |
| --- | --- | --- |
| A change appears in the wrong branch | The change was not committed before the move | Commit or stash before `git switch` |
| `error: pathspec 'name' did not match` | The branch does not exist | `git branch` to see names. `git switch -c name` to make it |
| `not fully merged` | The branch has commits that are not in the current branch | Join them first, or use `-D` if you do not need them |
| A file name and a branch name are the same | `git checkout name` can restore the file | Use `git switch name` |

## Recall questions

1. What is a branch in Git?
2. Does a new branch copy commits?
3. Which two commands make a branch and move to it?
4. What happens to a change that is not committed when you move to a different branch?
5. When does Git refuse to move to a different branch?
6. How do you rename a branch without a move to it?
7. Why does `git branch -d` refuse some branches? What does `-D` do?
8. Why does `git branch` show nothing after `git init`?

## Open questions

- The module number, the author, and the URL of the unit.
- The content of the screencasts and the IDE that the course uses.
