# MEPHI study vault instructions

## Scope and language

Owner: `milvalen`. This is a personal study vault.
Keep personal GitHub credentials separate from work credentials.
Do not add company or Logopolza content.
Do not invent course details, grades, deadlines, or completed work.

Use English for all communication, notes, documentation, templates, comments, and commit messages.
Use ASD-STE100 Issue 9 for technical prose.
Obey the [study note standard](00-standards/documentation-standard.md).
Use the [technical terms](00-standards/technical-terms.md) consistently.
STE clarity takes priority over compressed prose.
Keep exact commands, code identifiers, device paths, and interface labels.

## Sources and learning

Translate and summarize supplied material in English.
Do not store original text, transcripts, verbatim copies, or source attachments.
Keep only source references and external URLs for source information.

Separate source statements, assumptions, calculations, and open questions.
Cite the textbook edition and page, lecture date and slide, or official URL.
Never invent citations, measurements, attendance, grades, or review results.
Keep agent explanations as drafts until a source check or calculation supports them.

Keep each program in a separate folder under `02-programs`.
Keep lecture notes in their program’s course folder.
Keep the program’s graph color group current.
Do not treat an application as confirmed enrollment.
Add a separate concept note when it helps study. Link related notes in both directions.
Include recall questions, conditions of use, units, and common errors.
For problems, write an English task summary. Keep the attempt, reasoning, and checked answer.

For labs, keep observations separate from calculations and explanations.
Obey course rules about public access to assessed work.

## Structure and review

Use README.md as the home page. Keep folder indexes current.

Use relative Markdown links and the templates in `90-templates`.
Use only necessary YAML properties. Do not require community plugins.

Do not create course folders from guessed subjects.
Keep unresolved questions visible.

Before a note move, search the vault and workspace scripts for the old path.
Update affected links and references. Run the validator.
Review changed prose against ASD-STE100 rules and word meanings.
A language review does not change the date of an earlier technical check.

## Git and publication

Use `main` as the working and default branch.
Review the diff before each commit. Include only intended changes.
Run `python3 tools/validate-vault.py` before publication.
Run relevant sync checks after a change to sync code.
The owner permits routine documentation commits and pushes.

Do not force-push or overwrite unrelated changes.

The repository is public at the owner's request.
Publish only personal notes and material permitted for public sharing.
Do not store credentials, private keys, student identifiers, or private records about other people.

## Windows mirror

Linux contains the main editable vault. Windows contains a one-way copy.
Windows changes do not return to Linux.
The sync service keeps newer Windows files and makes backups before replacement or deletion.
Edit the Linux notes to avoid differences between copies.

Only graph color groups are shared automatically.
Other device settings remain local.
Keep logs and backups outside this repository.
Track only specified portable Obsidian settings.
Exclude workspace state, caches, and plugins.
Refer to [Windows synchronization](00-standards/windows-vault-sync.md).
