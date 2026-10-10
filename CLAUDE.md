# MEPHI study vault instructions

## Scope and ownership

This vault holds personal study notes, course maps, worked problems, laboratory notes and exam preparation. Owner: `milvalen`. Keep personal GitHub identity separate from work accounts. Do not import Logopolza or company content. The curriculum, semester, teachers and deadlines are unknown until the owner supplies evidence.

## Learning and evidence

Follow [the note standard](00-standards/documentation-standard.md). Use the language of the course material; preserve Russian terms and exact quotations. Use English for tooling and commit messages. Summarize in the student's own words. Separate source statements, derivations, assumptions and open questions. Cite textbook edition and page, lecture date/slide, or official URL. Never invent citations, grades, attendance, completed reviews or laboratory measurements. Mark AI-created explanations as drafts until checked against a source or a reproducible calculation.

Keep course-specific lecture notes within their course. Extract reusable concepts only when useful and link both ways. Include recall questions, conditions of applicability, units and common errors. For exercises, retain the statement, attempt, reasoning and checked answer; for labs, preserve raw observations separately from analysis. Preserve original attachments and respect course restrictions on sharing assessed work.

## Organization and maintenance

Use the README as the home page and maintain folder indexes. Use relative Markdown links so GitHub and Obsidian both work. Use minimal YAML properties and templates from `90-templates`. Avoid mandatory community plugins. Do not create empty course hierarchies based on guessed subjects. Keep unresolved questions explicit. Before moving a note, search the whole vault and workspace tooling for old paths, update links and run the validator.

## Git and Windows mirror

Use `main` as the working and default branch. Review intended changes and run `python3 tools/validate-vault.py` plus relevant sync checks before commits. Routine documentation commits and pushes are permitted by the owner; do not force-push or overwrite unrelated changes. Repository visibility is private.

Linux is the canonical editable vault. Windows is a one-way reading mirror; edits there do not return to Linux. The mirror preserves newer Windows files, backs up replaced/deleted files and excludes personal Obsidian state. Only graph color groups are shared automatically. Edit canonical notes in Linux to avoid conflicts. Sync scripts are documented in [the Windows guide](00-standards/windows-vault-sync.md).

Never store credentials, private keys, student identifiers or private third-party records. Keep service logs and backups outside this repository. Track only explicit portable Obsidian configuration; exclude workspace, cache and plugins.
