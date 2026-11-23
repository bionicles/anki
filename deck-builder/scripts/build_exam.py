"""Publish an exam card table and component map as an Anki study bundle."""

import argparse
import csv
import hashlib
import json
import re
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from build_deck import require_text, rendered
import genanki

FIELDS = ["CardID", "Question", "Answer", "Explanation", "Source"]
CARD_COLUMNS = FIELDS + ["Tags"]
MAP_COLUMNS = ["outline_version", "outline_source", "domain", "objective", "component",
               "component_status", "card_ids", "coverage_note"]
MODEL = genanki.Model(
    1816438521, "Exam Study (anki-deck-builder v1)",
    fields=[{"name": name} for name in FIELDS],
    templates=[{"name": "Recall", "qfmt": "{{Question}}",
                "afmt": "{{FrontSide}}<hr id=answer>{{Answer}}"
                        "{{#Explanation}}<p>{{Explanation}}</p>{{/Explanation}}"
                        "<small>{{Source}}</small>"}],
    css=".card {font: 20px sans-serif; text-align: left; line-height: 1.45} "
        "small {font-size: 0.75em}",
)


def table(path, columns, delimiter):
    with path.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        if reader.fieldnames != columns:
            raise ValueError(f"{path}: expected columns {columns}")
        rows = list(reader)
    for n, row in enumerate(rows, start=2):
        if None in row or None in row.values():
            raise ValueError(f"{path} row {n}: incorrect field count")
        for key, value in row.items():
            row[key] = require_text(value, f"{path} row {n} {key}") if value.strip() else ""
    if not rows:
        raise ValueError(f"{path} contains no records")
    return rows


def token(value, label):
    if not re.fullmatch(r"[\w.-]+", value):
        raise ValueError(f"{label}: use a single ID with letters, digits, dots, dash or underscore")
    return value


def check(cards, coverage):
    by_id, cues = {}, set()
    for row in cards:
        key = token(row["CardID"], "CardID")
        for name in ["Question", "Answer", "Source"]:
            require_text(row[name], f"{key} {name}")
        cue = " ".join(row["Question"].casefold().split())
        if key in by_id or cue in cues:
            raise ValueError(f"{key}: repeated ID or question")
        cues.add(cue)
        by_id[key] = row
    mappings, components, status = defaultdict(set), set(), defaultdict(list)
    for row in coverage:
        for col in ["outline_version", "outline_source", "component"]:
            require_text(row[col], col)
        domain, objective = (token(row[k], k) for k in ("domain", "objective"))
        part = (domain, objective, row["component"].casefold())
        if part in components:
            raise ValueError(f"repeated component: {part}")
        components.add(part)
        state = row["component_status"]
        ids = row["card_ids"].split()
        if state not in ("covered", "partial", "gap"):
            raise ValueError(f"{part}: choose covered, partial, or gap")
        if (state == "gap") != (not ids) or len(ids) != len(set(ids)):
            raise ValueError(f"{part}: check card_ids against component_status")
        if state != "covered" and not row["coverage_note"]:
            raise ValueError(f"{part}: describe the remaining gap")
        for key in ids:
            if key not in by_id:
                raise ValueError(f"{part}: unknown card ID {key}")
            mappings[key].update((f"domain::{domain}", f"objective::{objective}"))
        status[(domain, objective)].append(state)
    for key, row in by_id.items():
        if key not in mappings:
            raise ValueError(f"{key} has no component mapping")
        tags = set(row["Tags"].split())
        if not any(t.startswith("type::") and t[6:] for t in tags):
            raise ValueError(f"{key} needs a type:: tag")
        declared = {t for t in tags if t.startswith(("domain::", "objective::"))}
        if declared - mappings[key]:
            raise ValueError(f"{key}: tag conflicts with the component map: {declared - mappings[key]}")
        row["Tags"] = " ".join(sorted(tags | mappings[key]))
    return {key: "full" if all(s == "covered" for s in parts) else
            "gap" if all(s == "gap" for s in parts) else "partial"
            for key, parts in status.items()}


def publish(args):
    if args.output.exists():
        raise ValueError("choose a new output directory for this build")
    deck_name = require_text(args.deck, "deck")
    if any(c in deck_name for c in "\r\n\t"):
        raise ValueError("deck name must be one line")
    namespace = token(args.namespace, "namespace")
    cards = table(args.cards, CARD_COLUMNS, "\t")
    coverage = table(args.coverage, MAP_COLUMNS, ",")
    status = check(cards, coverage)
    digest = hashlib.sha256(("anki-exam/" + namespace).encode()).digest()
    deck = genanki.Deck(1_000_000_000 + int.from_bytes(digest[:6], "big"), deck_name)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.output.parent) as temp:
        work = Path(temp).resolve()
        out = work / "out"
        out.mkdir()
        with (out / f"{namespace}.tsv").open("w", encoding="utf-8", newline="") as fh:
            fh.write(f"#separator:Tab\n#html:true\n#notetype:{MODEL.name}\n#deck column:2\n"
                     "#guid column:1\n#tags column:8\n")
            fh.write("#columns:" + "\t".join(["GUID", "Deck", *CARD_COLUMNS]) + "\n")
            writer = csv.writer(fh, delimiter="\t", quoting=csv.QUOTE_ALL, lineterminator="\n")
            for n, row in enumerate(cards, 1):
                fields = [rendered(row[name]) for name in FIELDS]
                guid = genanki.guid_for(json.dumps(["anki-exam", namespace, row["CardID"]]))
                deck.add_note(genanki.Note(model=MODEL, fields=fields, tags=row["Tags"].split(),
                                           guid=guid, due=n))
                writer.writerow([guid, deck_name, *fields, row["Tags"]])
        with (out / "coverage.csv").open("w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=MAP_COLUMNS + ["objective_status"])
            writer.writeheader()
            for row in coverage:
                writer.writerow(dict(row, objective_status=status[(row["domain"], row["objective"])]))
        previous = tempfile.tempdir
        try:
            tempfile.tempdir = str(work)
            genanki.Package(deck).write_to_file(out / f"{namespace}.apkg")
        finally:
            tempfile.tempdir = previous
        out.rename(args.output)
    domain_counts = Counter(tag[8:] for row in cards for tag in row["Tags"].split()
                            if tag.startswith("domain::"))
    print(f"{len(cards)} cards. Cards per mapped domain: {dict(domain_counts)}")
    print(f"Objectives: {dict(Counter(status.values()))}. Files: {args.output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cards", type=Path)
    parser.add_argument("coverage", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--deck", required=True)
    parser.add_argument("--namespace", required=True)
    args = parser.parse_args()
    try:
        publish(args)
    except (ValueError, OSError, csv.Error) as exc:
        parser.exit(1, f"build_exam: {exc}\n")


if __name__ == "__main__":
    main()
