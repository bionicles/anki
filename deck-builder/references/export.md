# Manifest and import guide

Save this example as `notes.json`. Run the command in SKILL.md with a destination ending in `.apkg` or `.tsv`. A deck may mix note types.

```json
{
  "deck": "Astronomy::Foundations",
  "namespace": "astronomy-foundations-en",
  "notes": [
    {"id": "eclipse-geometry", "type": "cloze", "text": "A lunar eclipse occurs when {{c1::Earth}} lies between the Sun and the {{c2::Moon}}.", "extra": "Diagram 2, class handout", "tags": ["topic::eclipses"]},
    {"id": "eclipse-phase", "type": "basic", "front": "At which lunar phase can a lunar eclipse occur?", "back": "Full moon.", "tags": ["topic::eclipses"]},
    {"id": "moon-es", "type": "reversed", "front": "la Luna", "back": "the Moon", "tags": ["language::es"]}
  ]
}
```

This builds three notes and five cards. Choose a unique, durable namespace per project. Give each concept a permanent ID independent of order and wording. Within a package series keep the namespace, IDs, and note types stable. Edits then match existing notes under Anki's update settings. Assume a type change or removal needs separate reconciliation. Removing a note from a package does not delete someone's imported note.

**Fields.** Supply literal Unicode text. The exporter escapes HTML and turns line breaks into visible breaks. Basic and reversed take `front` and `back`. Cloze takes `text` and optional `extra`. The exporter supports flat, positive-numbered deletions with optional hints, e.g. `{{c1::Mercury::planet}}`. Put supporting material in the Basic back or Cloze extra. A reversed note tests all of each side. Tags are an optional array of single tokens.

**Media in packages.** Attach local files with `front_media` or `back_media` arrays, e.g. `"front_media": ["images/masked.png"]`. Paths are relative to the manifest. These fields append media to the first or second note field, respectively. Use common image or audio formats. The package contains content-named files that also avoid exposing descriptive filenames. For an editable TSV with media, provide the media separately and map literal Anki references in a custom export, or deliver a package alongside the requested text.

**Import.** Open the package in Anki or select File → Import. To revise it, rebuild from the same manifest, re-import, and choose the update behavior appropriate to the requested changes. TSV uses Anki's file headers (2.1.54+) and English stock model names. Preview the note type, deck, two fields, and tags before import. Map localized or renamed models explicitly. Text import matches on the first field by default, so changing a cue may create a new note. Use one format consistently across revisions.

**Existing decks.** Preserve original GUIDs, model IDs, ordered fields, and templates when updating someone else's export. A fresh manifest cannot recreate those identities. Start from the caller's exported notes or a disposable collection imported from their package, apply targeted edits, and export again. Use a supplied CSV dialect or custom note schema when requested.

[Anki text import](https://docs.ankiweb.net/importing/text-files.html) · [Anki note types and cloze editing](https://docs.ankiweb.net/editing.html) · [genanki package writer](https://github.com/kerrickstaley/genanki)

## One card with alternative prompts

Add a `varied` note to a manifest when the same short answer and feedback fit every front. For example:

```json
{
  "id": "relative-price",
  "type": "varied",
  "front": "A stock/benchmark price ratio rises over a week. How did the stock perform relative to the benchmark?",
  "variants": [
    "One share buys more units of the benchmark on Friday than on Monday. Which asset had the higher price return?",
    "Over the same interval, the stock lost 2% and its benchmark lost 6%. Which one outperformed on price?"
  ],
  "back": "The stock outperformed the benchmark on price."
}
```

The package installs the custom note type. The front chooses at random from the canonical prompt and the saved alternatives, so a wording can repeat. With scripting disabled, the canonical prompt stays visible. The answer side shows the shared answer and any back media. Front media applies to every wording. The prompts work offline without an AI account or API key. The single scheduled card has one review history. Give a substantially harder version its own card if its performance matters independently.

For a manifest containing varied notes, use the same pinned genanki environment for both the package and TSV. The TSV includes package note GUIDs and packaged model names. Import the package first to install **Deck Builder · Varied prompt**. In a mixed-model export, preview the field mappings for each note type. Anki documents client differences in template scripting, so preview the intended study client. [Anki template scripting](https://docs.ankiweb.net/templates/styling.html#javascript) · [Anki card generation](https://docs.ankiweb.net/templates/generation.html)
