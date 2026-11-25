"""Build the CMT package and check a real Anki import, including the chart images."""
import argparse
import csv
import json
import re
import sys
import tempfile
from pathlib import Path

import genanki

PROJECT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT.parents[1] / "deck-builder" / "scripts"))
sys.path.insert(0, str(PROJECT.parent))
from finance_media import apply_figure, read_figures
from build_deck import rendered
from build_exam import CARD_COLUMNS, FIELDS, MAP_COLUMNS, check, table

GUIDE = "https://cmtassociation.org/wp-content/uploads/2025/12/CMT-PROGRAM-GUIDE-2026-1.pdf"
AUDIT_COLUMNS = ["level", "guide_page", "unit_ordinal_in_level", "deck_topic", "objective_ordinal_in_unit",
                 "objective_summary", "review_result", "evidence_card_ids"]
DECK = "Chartered Market Technician"
NAMESPACE = "CMT"
MODEL = genanki.Model(
    1727294059, "CMT · short answer",
    fields=[{"name": name} for name in FIELDS + ["Chart"]],
    templates=[{"name": "Recall", "qfmt": "{{Question}}{{#Chart}}<div>{{Chart}}</div>{{/Chart}}",
                "afmt": "{{FrontSide}}<hr id=answer>{{Answer}}"
                        "{{#Explanation}}<p>{{Explanation}}</p>{{/Explanation}}<footer>{{Source}}</footer>"}],
    css=".card{font:20px/1.5 sans-serif;text-align:left;max-width:40em;margin:1em auto;padding:0 12px}"
        " img{width:min(100%,600px);height:auto} footer{margin-top:1em;font-size:.7em;overflow-wrap:anywhere}",
)


def prepare():
    cards = table(PROJECT / "cards.tsv", CARD_COLUMNS, "\t")
    coverage = table(PROJECT / "components.csv", MAP_COLUMNS, ",")
    audit = table(PROJECT / "objective-audit.csv", AUDIT_COLUMNS, ",")
    by_id = {card["CardID"]: card for card in cards}
    domains = {row["objective"]: row["domain"] for row in coverage}
    observed = set()
    for row in audit:
        level = row["level"]
        unit = int(row["unit_ordinal_in_level"])
        number = int(row["objective_ordinal_in_unit"])
        key = (level, unit, number)
        if key in observed:
            raise ValueError(f"Duplicate exam objective {key}")
        observed.add(key)
        evidence = row["evidence_card_ids"].split()
        state = {"direct": "covered", "partial": "partial", "no match": "gap"}[row["review_result"]]
        if len(evidence) != len(set(evidence)) or bool(evidence) != (state != "gap"):
            raise ValueError(f"Inconsistent evidence for {key}")
        kinds = sorted({tag.removeprefix("type::") for cid in evidence
                        for tag in by_id[cid]["Tags"].split() if tag.startswith("type::")})
        if state == "covered" and (len(evidence) < 3 or len(kinds) < 2):
            raise ValueError(f"{key}: direct coverage requires three exercises in at least two formats")
        for cid in evidence:
            card = by_id[cid]
            tags = card["Tags"].split()
            if f"level::{level}" not in tags:
                raise ValueError(f"{cid}: objective {key} is unavailable in its level filter")
            tags.append(f"los::{level}::{unit:02d}::{number:02d}")
            card["Tags"] = " ".join(tags)
        coverage.append(dict(
            outline_version="2026",
            outline_source=GUIDE + "#page=" + row["guide_page"],
            domain=domains[row["deck_topic"]], objective=f"{level}-{unit:02d}-{number:02d}",
            component=row["objective_summary"], component_status=state,
            card_ids=row["evidence_card_ids"],
            coverage_note={"gap": "No matched exercise.", "partial": "Some components or prerequisites practiced.",
                           "covered": "Direct practice of the published objective."}[state]
                          + f" Linked exercises: {len(evidence)}. Formats: {', '.join(kinds) or 'none'}.",
        ))
    expected_counts = {"I": 244, "II": 125, "III": 109}
    for level, count in expected_counts.items():
        if sum(key[0] == level for key in observed) != count:
            raise ValueError(f"Expected {count} published {level} objectives")
    statuses = check(cards, coverage)
    notes = []
    figures = read_figures(PROJECT)
    if figures.keys() - by_id.keys():
        raise ValueError("Unknown CMT card in figures.tsv")
    media = {r["Filename"]: PROJECT / "media" / r["Filename"] for r in figures.values()}
    for card in cards:
        fields = {name: rendered(card[name]) for name in FIELDS}
        figure = figures.get(card["CardID"])
        tags = apply_figure(fields, card["Tags"], figure)
        match = re.fullmatch(r"CMT-chart-(\d+)", card["CardID"])
        chart = ""
        if match:
            assert figure is None
            tags += " medium::figure visual::question"
            name = f"cmt_study_{match[1]}.png"
            media[name] = PROJECT / "media" / name
            chart = f'<img src="{name}" alt="Market chart for this question">'
        fields = [fields[name] for name in FIELDS] + [chart]
        guid = genanki.guid_for(json.dumps(["anki-exam", NAMESPACE, card["CardID"]]))
        notes.append((guid, fields, tags))
    mapped = [dict(row, objective_status=statuses[row["domain"], row["objective"]]) for row in coverage]
    return notes, media, mapped


def build(directory, notes, media, mapped):
    if directory.exists():
        raise ValueError(f"Choose a fresh release directory: {directory}")
    with tempfile.TemporaryDirectory(dir=directory.parent) as temp:
        out = Path(temp) / "out"
        out.mkdir()
        deck = genanki.Deck(1411098159, DECK)
        with (out / "CMT.tsv").open("w", encoding="utf-8", newline="") as fh:
            fh.write(f"#separator:Tab\n#html:true\n#notetype:{MODEL.name}\n#deck column:2\n#guid column:1\n#tags column:9\n")
            fh.write("#columns:" + "\t".join(["GUID", "Deck", *FIELDS, "Chart", "Tags"]) + "\n")
            writer = csv.writer(fh, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_ALL)
            for due, (guid, fields, tags) in enumerate(notes, 1):
                deck.add_note(genanki.Note(model=MODEL, fields=fields, tags=tags.split(), guid=guid, due=due))
                writer.writerow([guid, DECK, *fields, tags])
        package = genanki.Package(deck)
        package.media_files = [str(path) for path in media.values()]
        package.write_to_file(out / "CMT.apkg")
        with (out / "coverage.csv").open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=MAP_COLUMNS + ["objective_status"])
            writer.writeheader()
            writer.writerows(mapped)
        out.rename(directory)


def verify(directory, notes, media, mapped):
    from anki.collection import Collection
    from anki.import_export_pb2 import ImportAnkiPackageRequest, ImportCsvRequest

    directory = directory.resolve()
    assert table(directory / "coverage.csv", MAP_COLUMNS + ["objective_status"], ",") == mapped
    expected = {guid: (fields, tags) for guid, fields, tags in notes}
    tsv = directory / "CMT.tsv"
    with tsv.open(encoding="utf-8", newline="") as fh:
        reader = csv.reader((s for s in fh if not s.startswith("#")), delimiter="\t")
        assert list(reader) == [[g, DECK, *f, t] for g, f, t in notes]
    with tempfile.TemporaryDirectory() as temp:
        col = Collection(str(Path(temp) / "temp.anki2"))
        try:
            col.import_anki_package(ImportAnkiPackageRequest(package_path=str(directory / "CMT.apkg")))
            def snapshot():
                ids = {}
                for cid in col.find_cards(""):
                    card = col.get_card(cid)
                    note = card.note()
                    fields, tags = expected[note.guid]
                    assert fields == note.fields and set(tags.split()) == set(note.tags)
                    assert col.decks.name(card.did) == DECK and note.note_type()["name"] == MODEL.name
                    assert note["Question"] in card.question() and note["Answer"] in card.answer()
                    assert note["Chart"] in card.question()
                    if "visual::worked" in note.tags:
                        assert "<img" not in card.question() and "<img" in card.answer()
                    if "visual::question" in note.tags:
                        assert "<img" in card.question()
                    assert note.guid not in ids
                    ids[note.guid] = (note.id, cid)
                assert ids.keys() == expected.keys()
                return ids
            before = snapshot()
            for name, path in media.items():
                assert Path(col.media.dir(), name).read_bytes() == path.read_bytes()
            for nid, _ in before.values():
                note = col.get_note(nid)
                note["Answer"] = "Temporary import check"
                col.update_note(note)
            meta = col.get_csv_metadata(str(tsv), None)
            result = col.import_csv(ImportCsvRequest(path=str(tsv), metadata=meta))
            assert len(result.log.updated) == len(notes) and snapshot() == before
        finally:
            col.close()
    print(f"Verified {len(notes)} notes and cards, {len(media)} charts, coverage and identity-preserving TSV updates.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["build", "verify"])
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    (build if args.action == "build" else verify)(args.directory, *prepare())
