---
name: anki-deck-builder
description: Build, revise, or audit study flashcards for Anki. Use for turning notes, PDFs, slides, vocabulary lists, or spreadsheets into reviewable cards, making cloze deletions or bidirectional cards, fixing an Anki import, mapping exam objectives to sourced cards and coverage.csv, and delivering editable TSV or a ready-to-import .apkg with local media. Also use when the user asks for a spaced-repetition deck without naming Anki. Scheduling advice, sync troubleshooting, live quizzes, and presentation decks are separate tasks.
---

# Anki deck builder

Deliver the requested deck and enough information to import and review it. Default to a downloadable `.apkg` for an unspecified deck file, UTF-8 TSV for an editable text import, and a small inline sample when the user asks for a preview. Honor any supplied schema, language, deck hierarchy, and learning direction.

For an exam or curriculum deck with coverage requirements, use the [exam workflow and reusable project brief](references/exam-decks.md). For exam preparation, plan several independent retrieval opportunities for each numbered skill. Revisit the same decision with changed evidence, constraints, and plausible alternatives. Respect explicit card limits and narrow requests. The exam workflow builds the package, editable TSV, and coverage map together. For a rebuildable project, deliver its authoring tables, scripts, and working `just build` and `just test` recipes.

## Decide what belongs on a card

1. Inspect the source first. For paginated material, retain page, slide, or section locators as you extract facts. Check diagrams, table headers, footnotes, and OCR symbols against the original. When the source is missing and fidelity to it matters, ask for it. For a topic-only request, use reliable references appropriate to the subject and identify the basis for the deck.
2. Map the learning goals to distinct facts, discriminations, or decisions. Prioritize those the learner will need to recall. For an exam, keep details the outline asks the learner to recall or that would change a tested decision. Put incidental dates, credits and anecdotes on the back when they help. A fixed card target alone gives a detail no study value. Keep an explicit limit in **generated cards** if the user asked for cards. If the evidence supports fewer, deliver what it supports and explain the gap.
3. Draft a cue that works when shuffled. Name the subject, direction, units, or conditions that distinguish the answer. Keep the graded answer short. Put examples, exceptions, and source locators after the answer. When a worked example introduces a calculation, interpretation or decision worth retrieving, check whether another card already tests it. Give an uncovered target its own self-contained prompt and stable ID. Preserve qualifiers and flag conflicting claims separately. Never invent a locator.
4. Pick the note type by what the learner must retrieve. Use Basic for a question, applied decision, or contrast. Use reversed notes only when both sides uniquely cue the other. Practice both directions when the learner needs both. If one direction needs a sense hint, a different audio placement or its own grading rule, write separately cued Basic notes. Use Cloze for completing a relationship in context. Reuse an index to hide parts together, and give independent targets different indices. Preview each resulting card for hints that reveal the answer.
5. For longer sources, work by section, compare the finished set against the learning goals, and remove overlaps across batches. Use the [card patterns](references/card-patterns.md) to choose between a reverse, a separately graded example and an optional offline wording variant. Audit existing decks for duplicate targets, answer leakage and incidental detail before adding reviews.

## Build the artifact

For a general-purpose deck, put the notes in a JSON manifest and run the bundled exporter. Set `SKILL_DIR` to this skill's absolute directory and place outputs in the user's requested destination. [Manifest and import guide](references/export.md) includes a working example, local media, and revision rules.

```sh
python3 "$SKILL_DIR/scripts/build_deck.py" notes.json deck.tsv
uv run --no-project --with genanki==0.13.1 python "$SKILL_DIR/scripts/build_deck.py" notes.json deck.apkg
```

Use an existing Python with genanki when available. Keep the manifest with a revisable package so future edits can reuse note identities. If a requested package dependency is unavailable, try an isolated environment. Clearly label any fallback TSV and give import steps. For custom models, existing exports, or native image occlusion, follow the user's actual schema and inspect original field mappings first. The bundled exporter covers Basic, reversed, Cloze and optional varied-prompt notes.

## Verify and hand off

- Check each answer against its source. Inspect ambiguous cues, answer leakage, near-duplicates, lost negations, units, and multilingual text. For large decks sample every section and note type after running structural checks across all notes.
- Check the actual artifact. For a package, import into a fresh disposable Anki collection when available and inspect both sides of representative cards plus media references. For TSV, inspect parsed rows, model/deck columns, tags, and field order in import preview. Distinguish a file-level check from a real import.
- Report the artifact path, note and generated-card counts, key omissions or unresolved ambiguities, and a specific import instruction. If an update is requested, verify by re-importing into a disposable copy and comparing counts and edited content. Leave a live collection alone unless the user asked to modify it.
