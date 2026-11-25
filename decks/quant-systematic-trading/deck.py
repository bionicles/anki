"""Build the systematic trading deck and audit it against its prespecified curriculum."""
import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[1] / "deck-builder" / "scripts"))
import build_exam


def load_inputs():
    cards = build_exam.table(ROOT / "cards.tsv", build_exam.CARD_COLUMNS, "\t")
    components = build_exam.table(ROOT / "components.csv", build_exam.MAP_COLUMNS, ",")
    domains = build_exam.table(ROOT / "curriculum.tsv", ["Domain", "Name", "Objectives"], "\t")
    expected = [(domain["Domain"], key) for domain in domains for key in domain["Objectives"].split()]
    actual = [(r["domain"], r["objective"]) for r in components]
    if Counter(expected) != Counter(actual) or len({k for _, k in expected}) != len(expected):
        raise ValueError("Coverage map must match every curriculum objective exactly once")
    by_id = {row["CardID"]: row for row in cards}
    flags = {key: set(row["Tags"].split()) for key, row in by_id.items()}
    figures = build_exam.table(ROOT / "figures.tsv", ["CardID", "Side", "Filename", "Description"], "\t")
    media = {"front": {}, "back": {}}
    for row in figures:
        key, side, name = (row[field] for field in ["CardID", "Side", "Filename"])
        if (side not in media or key not in by_id or key in media[side]
                or Path(name).name != name or not (ROOT / "media" / name).is_file()):
            raise ValueError(f"Invalid media mapping for {key}: {name}")
        media[side][key] = (ROOT / "media" / name, row["Description"])
    for key, tags in flags.items():
        for side, tag in [("front", "visual::question"), ("back", "visual::worked")]:
            if (key in media[side]) != (tag in tags):
                raise ValueError(f"{key}: figure on {side} and tag {tag} disagree")
        if ("medium::figure" in tags) != (key in media["front"] or key in media["back"]):
            raise ValueError(f"{key}: incorrect figure filter")
    files = {path for mapping in media.values() for path, _ in mapping.values()}
    if files != set((ROOT / "media").glob("*.png")):
        raise ValueError("Generated figures and the media directory differ")
    assigned = Counter()
    required_types = {"type::mechanism", "type::application", "type::diagnosis", "type::interpretation"}
    for row in components:
        ids = row["card_ids"].split()
        assigned.update(ids)
        types = {t for k in ids for t in flags[k] if t.startswith("type::")}
        steps = [key for key in ids if "practice::step" in flags[key]]
        transfers = [key for key in ids if "practice::transfer" in flags[key]]
        if steps or transfers:
            if len(steps) < 3 or len(transfers) != 1 or not any(key in media["front"] for key in steps):
                raise ValueError(f"Incomplete step and transfer practice for {row['objective']}")
            transfer = transfers[0]
            if transfer not in media["front"]:
                raise ValueError(f"Missing transfer chart for {transfer}")
            chart = media["front"][transfer][0]
            if sum(path == chart for mapping in media.values() for path, _ in mapping.values()) != 1:
                raise ValueError(f"{transfer} must have an independent example")
        if (len(set(ids)) < 4 or not required_types.issubset(types) or row["component_status"] != "covered"
                or not any(k in media["front"] for k in ids)
                or not any(k in media["back"] for k in ids)):
            raise ValueError(f"Insufficient practice for {row['objective']}")
    if assigned != Counter(by_id.keys()):
        raise ValueError("Each course card must practice exactly one curriculum objective")
    return media


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["build", "verify"])
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    args.cards = ROOT / "cards.tsv"
    args.components = args.coverage = ROOT / "components.csv"
    args.namespace = "Quant-Systematic-Trading"
    args.deck = "Quantitative and Systematic Trading"
    media = load_inputs()
    if args.action == "build":
        args.output = args.directory
        build_exam.publish(args, media["front"], media["back"])
    else:
        import verify_exam
        args.release = args.directory
        args.latest = False
        verify_exam.verify(args, media["front"], media["back"])


if __name__ == "__main__":
    main()
