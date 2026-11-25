# Anki deck builder and study decks

Build flashcards for Anki from a JSON manifest or use the exam workflow to link cards to an exam outline. The repository includes six ready-to-import decks with editable text exports and coverage maps.

From the repository root, give your agent this prompt. Replace `$TEST` with the exam name.

```text
/goal use the ./deck-builder skill and build me an anki deck for $TEST
```

The [deck-by-deck design review](decks/card-design-review.md) maps recall, reversals, cue variation and visual practice to the six decks. Try a candle-pattern question in the [CMT guide](decks/cmt/README.md#practice-reading-charts) or an option payoff in the [Series 65 guide](decks/series-65/README.md).

**Quantitative and Systematic Trading** covers 138 objectives in 16 domains, from point-in-time data through portfolio risk and execution. Try the order-queue question and browse the curriculum in the [course guide](decks/quant-systematic-trading/README.md), or [download the Anki package](decks/quant-systematic-trading/release/Quant-Systematic-Trading.apkg).

## Tutorial

### Build and import your first card

Use Python 3 and the Anki desktop app. From the repository root, save this as `notes.json`:

```json
{
  "deck": "Astronomy Demo",
  "namespace": "astronomy-demo",
  "notes": [
    {
      "id": "moon-orbit",
      "type": "basic",
      "front": "What does the Moon orbit?",
      "back": "Earth."
    }
  ]
}
```

Run:

```sh
python3 deck-builder/scripts/build_deck.py notes.json astronomy.tsv
```

In Anki, choose **File → Import** and select `astronomy.tsv`. Review the import preview for the **Astronomy Demo** deck and **Basic** note type. Import the file, then open the deck and review the card. The front asks what the Moon orbits and the back shows “Earth.”

## How-to guides

### Import a shipped exam deck

Download an `.apkg` from the table below and open it in Anki with **File → Import**. The package installs the deck and its custom note type. To work with the editable TSV, import the package first and review the TSV field mappings and duplicate handling in the import preview. Try updates in a disposable profile before applying them to your study collection.

### Export a standalone package from a manifest

With [uv](https://docs.astral.sh/uv/) installed, run the exporter against your manifest:

```sh
uv run --no-project --with genanki==0.13.1 python \
  deck-builder/scripts/build_deck.py notes.json astronomy.apkg
```

Keep the manifest's namespace, note IDs, and note types stable when revising the package. See the [manifest and export guide](deck-builder/references/export.md) for cloze notes, reversed cards, media, and re-import behavior.

### Build and verify an exam deck

Prepare `cards.tsv` and `components.csv` using the schemas in the [exam workflow](deck-builder/references/exam-decks.md). From the repository root, with those files present, run:

```sh
uv run --no-project --with genanki==0.13.1 python \
  deck-builder/scripts/build_exam.py cards.tsv components.csv release-1 \
  --deck "Sample Exam" --namespace Sample-Exam

uv run --no-project --with genanki==0.13.1 --with anki==26.9.4 python \
  deck-builder/scripts/verify_exam.py cards.tsv components.csv release-1 \
  --deck "Sample Exam" --namespace Sample-Exam
```

Use a new output directory for each build. For a standalone project with `just build` and `just test`, use the [template Justfile](deck-builder/assets/exam-project/Justfile) and follow the layout in the exam workflow. Series 65 uses its own note schema and includes rebuild and import-verification recipes. ACSM-CPT is a release snapshot with placeholder Justfile recipes.

## Reference

| Deck | Anki package | Editable TSV | Coverage map | Project notes |
| --- | --- | --- | --- | --- |
| ACSM Certified Personal Trainer | [ACSM-CPT.apkg](decks/acsm-cpt/ACSM-CPT.apkg) | [ACSM-CPT.tsv](decks/acsm-cpt/ACSM-CPT.tsv) | [coverage.csv](decks/acsm-cpt/coverage.csv) | [ACSM-CPT brief](decks/acsm-cpt/goal.md) |
| Series 65, early 2027 scope | [Series-65.apkg](decks/series-65/Series-65.apkg) | [Series-65.tsv](decks/series-65/Series-65.tsv) | [coverage.csv](decks/series-65/coverage.csv) | [Deck guide](decks/series-65/README.md) |
| AWS Security Specialty | [Package](decks/aws-security-specialty/release/AWS-Security-SCS-C03.apkg) | [TSV](decks/aws-security-specialty/release/AWS-Security-SCS-C03.tsv) | [Coverage](decks/aws-security-specialty/release/coverage.csv) | [Deck guide](decks/aws-security-specialty/README.md) |
| Chartered Market Technician | [Package](decks/cmt/release/CMT.apkg) | [TSV](decks/cmt/release/CMT.tsv) | [Coverage](decks/cmt/release/coverage.csv) | [Deck guide](decks/cmt/README.md) |
| Frontier ML | [Package](decks/frontier-ml/release/Frontier-ML.apkg) | [TSV](decks/frontier-ml/release/Frontier-ML.tsv) | [Coverage](decks/frontier-ml/release/coverage.csv) | [Deck guide](decks/frontier-ml/README.md) |
| Quantitative and Systematic Trading | [Package](decks/quant-systematic-trading/release/Quant-Systematic-Trading.apkg) | [TSV](decks/quant-systematic-trading/release/Quant-Systematic-Trading.tsv) | [Coverage](decks/quant-systematic-trading/release/coverage.csv) | [Course guide](decks/quant-systematic-trading/README.md) |

| Entry point | Inputs and outputs |
| --- | --- |
| [`build_deck.py`](deck-builder/scripts/build_deck.py) | JSON manifest → `.tsv` or `.apkg`. Supports Basic, reversed, Cloze and optional varied prompts. TSV export uses the Python standard library and package export requires `genanki`. |
| [`build_exam.py`](deck-builder/scripts/build_exam.py) | Authoring TSV and component CSV → an output directory with a package, an editable TSV, and a coverage CSV. Requires `genanki`. |
| [`verify_exam.py`](deck-builder/scripts/verify_exam.py) | Authoring inputs and an exam release → import and identity checks in a temporary Anki collection. Requires `genanki` and the `anki` Python package. |

The [deck-building skill](deck-builder/SKILL.md) describes the authoring workflow. The [card patterns](deck-builder/references/card-patterns.md) show how to turn draft material into prompts that work in shuffled review.

## Explanation

A package bundles the deck's note type and templates for import. A TSV keeps the card fields accessible for review and editing. The coverage map connects exam outline components to card IDs so a reviewer can trace which cards test a topic and where gaps remain.

Stable note identity helps keep review history attached to a card as its wording changes. The manifest exporter derives package identities from the namespace, note ID, and note type. The exam builder uses the namespace and card ID to give its package and TSV matching identities.

The README follows the four documentation types described by [Diátaxis](https://diataxis.fr/).

## License

The original code, documentation, and deck material are available under the [MIT License](LICENSE). Referenced third-party material remains under its respective terms.
