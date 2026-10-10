# Study note standard

[Home](../README.md)

Use clear titles and stable descriptive filenames. Keep one focused topic per concept note, while lecture notes retain the lecture's context. Link related ideas with a sentence that explains the relationship. Use course indexes to navigate; tags provide only broad categories.

For normal notes, use YAML properties `title`, `type`, `status`, `created`, `updated` and optionally `course`, `tags`, `review_due`. Use ISO dates. Types: course, lecture, concept, problem, lab, source, review. Status: draft or checked; checked means the stated explanation or calculation was actually verified. Indexes and instruction files need no properties. Quote template date variables in YAML. A review due date is a planning choice, not evidence that a review happened.

Record sources close to claims. A source note records author, title, edition/year, pages or slides, URL and access date where applicable. Distinguish quotations from paraphrases. Preserve original attachments under `05-sources/attachments`; link to them rather than duplicating files. Do not upload restricted material without permission.

Lecture notes include context, key claims, examples, unclear points and recall prompts. Concepts include meaning, assumptions, examples and connections. Problems include the original statement, attempt before solution, derivation, units, result verification and errors. Labs separate procedure, raw data, uncertainty and interpretation. Keep historical attempts and corrections visible.

Use active recall before looking at answers and revisit material over time. Adjust review intervals based on performance and exam dates; no universal fixed schedule is assumed. This workflow draws on [retrieval practice](https://www.learningscientists.org/retrieval-practice) and [spaced practice](https://www.learningscientists.org/posters). Portable properties, templates and links follow the [Obsidian properties](https://obsidian.md/help/properties), [Templates](https://obsidian.md/help/plugins/templates) and [internal links](https://obsidian.md/help/links) documentation, consulted on 2026-10-11.

Run `python3 tools/validate-vault.py` before publication. Check unresolved claims against the actual course sources; link validation does not verify academic correctness.
