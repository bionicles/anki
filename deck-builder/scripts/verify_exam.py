"""Import an exam bundle into a disposable Anki collection and check its contents."""

import argparse
import csv
import tempfile
from pathlib import Path

from anki.collection import Collection
from anki.import_export_pb2 import ImportAnkiPackageRequest, ImportCsvRequest

from build_exam import CARD_COLUMNS, FIELDS, MAP_COLUMNS, MODEL, card_fields, check, table


def snapshot(col, expected, deck_name, figures, answer_figures):
    notes = col.find_notes("")
    cards = col.find_cards("")
    if len(notes) != len(expected) or len(cards) != len(expected):
        raise ValueError(f"import produced {len(notes)} notes and {len(cards)} cards")
    ids = {}
    for cid in cards:
        card = col.get_card(cid)
        note = card.note()
        key = note["CardID"]
        if key not in expected or key in ids or col.decks.name(card.did) != deck_name:
            raise ValueError(f"unexpected card or deck: {key}")
        row = expected[key]
        if list(note.keys()) != FIELDS or note.note_type()["name"] != MODEL.name:
            raise ValueError(f"{key}: incorrect field schema or model")
        if note.fields != card_fields(row, figures, answer_figures):
            raise ValueError(f"{key}: imported fields differ from authoring input")
        if set(note.tags) != set(row["Tags"].split()):
            raise ValueError(f"{key}: imported tags differ")
        if note["Question"] not in card.question() or note["Answer"] not in card.answer():
            raise ValueError(f"{key}: review template failed to render the question or answer")
        if key in answer_figures:
            filename = answer_figures[key][0].name
            if filename in card.question() or filename not in card.answer():
                raise ValueError(f"{key}: worked figure must be visible only after reveal")
        ids[key] = (note.guid, note.id, cid)
    return ids


def verify(args, figures=None, answer_figures=None):
    figures = figures or {}
    answer_figures = answer_figures or {}
    release = args.release.resolve()
    if args.latest:
        candidates = sorted(p for p in release.glob("release-*") if p.is_dir())
        if not candidates:
            raise ValueError("no published release found; run just build first")
        release = candidates[-1]
    cards = table(args.cards, CARD_COLUMNS, "\t")
    mapping = table(args.components, MAP_COLUMNS, ",")
    statuses = check(cards, mapping)
    expected = {row["CardID"]: row for row in cards}
    published = table(release / "coverage.csv", MAP_COLUMNS + ["objective_status"], ",")
    wanted = [dict(row, objective_status=statuses[row["domain"], row["objective"]]) for row in mapping]
    if published != wanted:
        raise ValueError("published coverage no longer matches the component map")
    package = (release / f"{args.namespace}.apkg").resolve()
    tsv = (release / f"{args.namespace}.tsv").resolve()
    with tempfile.TemporaryDirectory() as temp:
        col = Collection(str(Path(temp) / "test.anki2"))
        try:
            col.import_anki_package(ImportAnkiPackageRequest(package_path=str(package)))
            for path, _ in set(figures.values()) | set(answer_figures.values()):
                assert (Path(col.media.dir()) / path.name).read_bytes() == path.read_bytes()
            before = snapshot(col, expected, args.deck, figures, answer_figures)
            with tsv.open(encoding="utf-8", newline="") as file:
                rows = csv.reader((line for line in file if not line.startswith("#")), delimiter="\t")
                expected_rows = [[before[key][0], args.deck, *card_fields(row, figures, answer_figures),
                                  row["Tags"]] for key, row in expected.items()]
                if list(rows) != expected_rows:
                    raise ValueError("TSV identities, deck, field values, tags or row order differ")
            # Make every note differ so the TSV must actually restore every answer.
            for _, nid, _ in before.values():
                note = col.get_note(nid)
                note["Answer"] += " [verification edit]"
                col.update_note(note)
            meta = col.get_csv_metadata(str(tsv), None)
            result = col.import_csv(ImportCsvRequest(path=str(tsv), metadata=meta))
            if snapshot(col, expected, args.deck, figures, answer_figures) != before:
                raise ValueError("TSV import changed note or card identities")
            if len(result.log.updated) != len(expected):
                raise ValueError("TSV did not update every note")
        finally:
            col.close()
    print(f"Verified {len(expected)} notes/cards, TSV updates and coverage: {release}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cards", type=Path)
    parser.add_argument("components", type=Path)
    parser.add_argument("release", type=Path)
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--deck", required=True)
    parser.add_argument("--latest", action="store_true")
    args = parser.parse_args()
    try:
        verify(args)
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(1, f"verify_exam: {exc}\n")


if __name__ == "__main__":
    main()
