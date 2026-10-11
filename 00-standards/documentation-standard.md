# Study note standard

[Home](../README.md) · [Technical terms](technical-terms.md)

## Language standard

Use English for all communication and vault content. Use ASD-STE100 Issue 9, dated 2025-01-15, for technical prose.
This requirement includes notes, instructions, comments, templates, and commit messages.
Translate material from other languages. Write an English summary.

Do not save original source text, transcripts, verbatim copies, or source documents.
Keep source references and external URLs. Keep exact commands, code identifiers, and device paths.

Use the [official Issue 9 standard](https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf) for word meanings and grammar checks.
The [official STE website](https://www.asd-ste100.org/) identifies the current issue.
The following rules are a local summary, not a replacement for the standard.

- Use dictionary words with their approved meanings and parts of speech.
- Use defined technical nouns and technical verbs for computing concepts.
- Use one term for one concept. Refer to [Technical terms](technical-terms.md).
- Add every new technical term to [Technical terms](technical-terms.md) in the same change that first uses it.
- Define its meaning and permitted noun or verb form.
- Use simple verb forms and active voice. Use passive voice only when the person or system that does the action is unknown.
- Limit instruction sentences to 20 words. Give one instruction per sentence.
- Limit descriptive sentences to 25 words. Limit each paragraph to six sentences and one topic.
- Put a necessary condition before its instruction.
- Do not use semicolons in prose. Keep syntax punctuation in commands and configuration unchanged.
- Do not use phrasal verbs, slang, or noun groups that make the meaning unclear.
- Use American English spelling. Keep official product names and exact interface labels.

## Structure and links

Use clear titles and stable filenames. Keep one concept in each concept note.
Keep course-specific notes in their course folder. Keep the folder index current.
Use relative Markdown links. Explain the relationship between linked concepts.
Use tags for broad groups. Do not require community plugins.

## Properties

Use these YAML properties for study notes:

| Property | Meaning |
| --- | --- |
| `title` | Note title |
| `type` | `course`, `lecture`, `concept`, `problem`, `lab`, `source`, or `review` |
| `status` | `draft` or `checked` |
| `created`, `updated` | Dates in ISO format |
| `course` | Course name, if applicable |
| `tags` | Broad subject groups, if useful |
| `review_due` | Planned review date, if useful |

Use `checked` only after a source check or a calculation check.
A language review does not verify academic facts or complete a lab.
Indexes and instruction files do not need properties.
Put template date variables in quotation marks in YAML.
A planned date does not prove that a review occurred.

## Sources and evidence

Put references near the statements they support.
Record the author, title, edition, page or slide, URL, and access date when known.
A source page contains reference data. It must not contain a copy of the source text.
Do not invent unknown course details or source references.

Keep the date and scope of each actual check.
Identify owner-reported observations, agent checks, and examples separately.
Do not describe an example as an executed procedure.
A prose change does not create new runtime evidence.

## Study content

| Note type | Required content |
| --- | --- |
| Lecture | Context, key ideas, examples, open questions, and recall questions |
| Concept | Meaning, conditions, examples, connections, and sources |
| Problem | English task summary, attempt, reasoning, units, answer check, and errors |
| Lab | Method, observed data, calculations, explanation, and limits |
| Review | Recall attempt, feedback, correction, and next planned review |

Keep previous student attempts and corrections available.
Keep measured data separate from its explanation.

Use active recall before you read the answer. Repeat study in separate sessions.
Select the next review date from results and exam needs. Do not assume one fixed schedule works for every topic.
Refer to [retrieval practice](https://www.learningscientists.org/retrieval-practice) and [spaced practice](https://www.learningscientists.org/posters).
The agent read these learning references on 2026-10-11.

Use Obsidian's portable [properties](https://obsidian.md/help/properties), [Templates](https://obsidian.md/help/plugins/templates), and [links](https://obsidian.md/help/links).
The agent read these Obsidian references on 2026-10-11.

## Review before publication

1. Review the changed prose against the writing rules and dictionary.
2. Check technical terms against the glossary. Add an entry for each new technical term.
3. Check claims against their sources or recorded evidence.
4. Run `python3 tools/validate-vault.py`.
5. Review the Git diff.

A link check or sentence-length check does not prove full ASD-STE100 compliance.
