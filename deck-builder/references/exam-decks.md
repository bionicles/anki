# Exam and curriculum decks

Use this workflow when coverage of a syllabus, exam outline, or standard is part of success. It produces a package, editable Anki TSV, and a component-level coverage CSV from two plain tables. One independently graded question produces one card. For an existing deck with a different schema, retain its original model and IDs.

## Reusable project brief

Adapt this short brief as `goal.md` when the user asks for a prompt or project specification. Fill in the brackets from their request.

> Build a complete, importable Anki deck for [exam or curriculum] for [audience and sitting date]. Use [official outline and edition] and check for notices effective on the target date. Aim for [card range] with [domain priorities]. Map each objective and its component concepts before writing cards. Write original recall questions, worked calculations, and decision scenarios appropriate to each objective. Give every card a stable ID, one gradable answer, an explanation when useful, and a locator supporting the answer. Deliver [name].apkg, an editable [name].tsv, and coverage.csv. Verify the import, package/text parity, calculations, and coverage links. Report domain counts and unresolved gaps.

## Plan and author

1. Identify the target sitting, authoritative outline, effective version, domains, weights, and amendment notices. Resolve differences between publication, adoption, and testing dates. Inventory all objectives in their published order. Split named subskills, list elements, calculations, and decision rules into separately assessable components before generating cards.
2. Allocate a flexible card budget by weight and breadth. Use stable identifiers independent of row order. Build in domain-sized batches. Give application objectives a scenario with enough facts to support one best action. For calculations state givens, units, and rounding, and recompute the answer independently. Track every card touched by an amendment and recheck the wording, answer, and rationale against the applicable provision.
3. Cite a specific page, section, table, rule, or slide for each answer. The outline is the authority for scope. Look up the substantive source that establishes the answer. Preserve relevant dates and exceptions. Leave unsupported components as explicit gaps.
4. Enter exactly these header names in two authoring files. Use a TSV/CSV writer for fields containing delimiters or line breaks.

| File | Columns in order |
| --- | --- |
| `cards.tsv` (tab-separated) | `CardID`, `Question`, `Answer`, `Explanation`, `Source`, `Tags` |
| `components.csv` (comma-separated) | `outline_version`, `outline_source`, `domain`, `objective`, `component`, `component_status`, `card_ids`, `coverage_note` |

Use plain Unicode text in both inputs. `Source` holds the citation locator and a URL when available. Give each card a `type::recall`, `type::calculation`, `type::scenario`, or similarly meaningful tag. Use compact IDs for domain and objective. List linked card IDs separated by spaces. Mark a component `covered` only if the linked questions actually require the learner to retrieve it. Use `partial` for mapped but incomplete evidence and `gap` for a component with no card. State what is missing in `coverage_note`. One card can support several rows when its question genuinely tests each.

## Overlearning a numbered skill

Map the published skill IDs before allocating extra depth by domain weight. For each skill, identify a decision a learner should make, a nearby alternative they could confuse with it, and evidence that would change the decision. A useful sequence starts with recall, applies the rule in a new setting, then asks the learner to diagnose a failure or recognize an exception. Split broad skills into their component decisions and revisit difficult ones from several angles. Follow an explicit sample size or one-card-per-component request when given.

For example, after asking which credential a client needs, give the client a valid credential with the wrong scope and ask what fails. Then change the failure to expiry and ask which credential must be renewed. Each card should still work when encountered alone. A new company name or a reversed question adds little if the same keyword gives away every answer.

Publicly released older practice questions can identify durable distinctions or realistic distractors. Write original scenarios, change the evidence that determines the answer, and verify each rule against the current syllabus and primary source. Cite the current source on the answer side. Discard retired capabilities or identify their eligibility restrictions.

Audit the exported cards grouped by published skill ID. Count distinct cards and inspect the actual retrievals in each group for breadth, decisions, and near-duplicates. Check the weakest skill in each domain before adding depth to the strongest. Report the per-skill range, domain counts, uncovered components, and the source of any limits. A card count measures available practice. Demonstrated mastery requires learner performance on fresh prompts.

## Build and audit

```sh
uv run --with genanki==0.13.1 python "$SKILL_DIR/scripts/build_exam.py" \
  cards.tsv components.csv release-1 --namespace Sample-Exam --deck "Sample Exam"
```

Pick a new output directory for each release. Keep the namespace, card IDs, and model stable across revisions. The builder adds domain and objective tags, checks coverage references in both directions, and derives objective status. The exported package and TSV use the same note GUIDs, fields, and review template. Import the package first to install the note type. Edit the authoring tables for rebuilds or edit the delivered TSV and import it to update those notes.

Compare the source outline with the map to find omitted components. Inspect the cards behind each “covered” claim. Recalculate problems, read a scenario from each application objective, and sample factual answers and source locators across every domain. Import the package in a disposable collection, then import the TSV there and verify unchanged counts, fields, and visible answers. Reconcile projected vs actual domain counts (a cross-domain card counts in each mapped domain), fully covered objectives, partial objectives, and gaps. Include limitations in the handoff.

## Rebuildable project layout

For a reusable exam project, leave `cards.tsv`, `components.csv`, a copy of [the Justfile](../assets/exam-project/Justfile), and a `scripts/` folder containing `build_exam.py`, `build_deck.py`, and `verify_exam.py` from this skill. Set the deck name and permanent namespace at the top of the Justfile. With Python 3, uv, and just available, run from that project directory:

```sh
just build
just test
```

Each build prints a new release directory containing the three deliverables. The test imports the latest release into a temporary Anki collection, compares it to the authoring tables, edits its answers, and uses the TSV to restore them. This checks that a real text update preserves note and card identities. The recipes invoke Python directly through uv, which supplies the pinned dependencies. Keep the authoring tables, scripts, and recipes with the project so a future build can run independently of this skill installation.
