---
title: Git merge conflicts
type: lecture
status: draft
program: software-engineering
course: Java Programming
created: 2026-11-12
updated: 2026-11-12
---
# Git merge conflicts

[Java Programming](java-programming.md) · [Git branches](git-branches.md) · [Standard library](standard-library.md) · [Home](../../../../README.md)

## Context and evidence

The owner supplied this unit text on 2026-11-12. It follows the [Git branches unit](git-branches.md). It ends with a practice check.
Its module number, author, and URL are unknown. The text refers to four images and a screencast about conflict resolution. The owner did not supply them.
The vault keeps an English summary, not the original text or images.

The agent ran the commands below with Git 2.50.1 on macOS on 2026-11-12, in temporary repositories with no Git configuration.
The test file had 18 lines, with `String item = "master";` on line 15, as in the source example.

Sources for agent checks:

- [Pro Git, section 3.2, "Basic Branching and Merging"](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)
- [`git merge` documentation](https://git-scm.com/docs/git-merge)

## Skills for assessed work

1. Merge a branch into the current branch.
2. Know when a merge gives a conflict.
3. Read the conflict markers and resolve the conflict.
4. Stop a merge that you do not want to finish.

## Merge

`git merge name` joins the commits of the branch `name` into the current branch.

| Case | Result |
| --- | --- |
| The current branch has no new commits after the branch point | Fast-forward: Git moves the name of the current branch forward. No new commit |
| Both branches have new commits | Git makes a merge commit with two parent commits |

Agent check of the source example: the merge of `variant2` into `master` was a fast-forward. `master` had no new commits.
The merge of `variant1` then made a conflict.

## When a conflict occurs

Git compares three versions of the file: the merge base, the current branch, and the merged branch.
The merge base is the last commit that both branches share.
A conflict occurs when both branches changed the same lines, or lines next to each other, since the merge base.

| Change in `master` | Change in the branch | Agent check |
| --- | --- | --- |
| Line 3 | Line 15 | Merge without a conflict |
| Line 13 | Line 15 | Merge without a conflict |
| Line 14 | Line 15 | Conflict |
| Line 15 to `"x"` | Line 15 to `"x"` | Merge without a conflict: the changes are equal |
| Line 15 to `"variant2"` | Line 15 to `"variant1"` | Conflict |

## Resolve a conflict

Agent check: `git merge variant1` gave `CONFLICT (content): Merge conflict in Main.java` and exit code 1. `git status --short` showed `UU Main.java`.
The file then had these lines:

```text
<<<<<<< HEAD
String item = "variant2";
=======
String item = "variant1";
>>>>>>> variant1
```

- The part after `<<<<<<< HEAD` is the version of the current branch.
- The part before `>>>>>>> variant1` is the version of the merged branch.

1. Open the file. Find each `<<<<<<<` marker.
2. Keep one version, both versions, or a new version. Remove all three marker lines.
3. Compile and test the code.
4. `git add Main.java` marks the conflict as resolved.
5. `git commit`, or `git merge --continue`, records the merge commit.

To stop the merge, use `git merge --abort`. Agent check: after it, the file had `"variant2"` again and `git status` showed no changes.

To keep one side in all conflicts, use `git merge -X ours name` or `git merge -X theirs name`.
Agent check: `-X theirs` kept `"variant1"` with no conflict. Use this option only when you know that the other side is not necessary.

## Source corrections

| Source statement | Correction |
| --- | --- |
| A conflict occurs when the code at the merge is different from the code at the branch creation | That is true for almost every merge. A conflict occurs only when both branches changed the same or neighboring lines. Agent check: changes on lines 3 and 15 merged without a conflict |
| The branch "remembers" line 15 | Git does not keep a copy in the branch. It finds the merge base and compares the three versions |
| Changes on the same line in two branches can show an error | A conflict is not an error in the code. It is a decision that Git cannot make |
| "Changes can be overwritten, about this later" | The options `-X ours` and `-X theirs` do this. They can remove useful work |
| No steps after the edit | After the edit, `git add` and `git commit` are necessary. Without them, the merge stays incomplete |

## Common errors

| Symptom | Cause | Correction |
| --- | --- | --- |
| The code does not compile after a merge | A marker line stays in the file | Search for `<<<<<<<`, `=======`, and `>>>>>>>` |
| `Committing is not possible because you have unmerged files` | The file is not marked as resolved. Agent check: this message came from `git commit` before `git add` | Remove the markers, `git add`, then `git commit`. Or `git merge --abort` |
| Work of a colleague is missing | The conflict was resolved with one side only | Compare both versions before you remove one |
| Many conflicts at one time | Branches stayed separate for a long time | Merge the main branch into your branch frequently |

## Recall questions

1. What is a fast-forward merge?
2. What is the merge base?
3. Which changes cause a conflict? Do changes on lines 3 and 15 cause one?
4. What do `<<<<<<< HEAD`, `=======`, and `>>>>>>>` mark?
5. Which two commands finish a merge after you edit the file?
6. How do you stop a merge with a conflict?
7. What does `-X theirs` do, and why is it dangerous?

## Open questions

- The module number, the author, and the URL of the unit.
- The content of the screencast and of the practice check.
