"""Build an Anki package or importable UTF-8 text from a deck manifest."""

import argparse
import csv
import hashlib
import html
import json
import re
import tempfile
import unicodedata
from pathlib import Path

MODELS = {"basic": "Basic", "reversed": "Basic (and reversed card)", "cloze": "Cloze",
          "varied": "Deck Builder · Varied prompt"}
VARIED_FRONT = """<div id="adb-prompt">{{Front}}</div>
<div hidden id="adb-alternatives">{{Alternatives}}</div>
{{PromptMedia}}
<script>
(function () {
    var alternatives = document.getElementById("adb-alternatives").children;
    var choice = Math.floor(Math.random() * (1 + alternatives.length));
    if (choice > 0) {
        document.getElementById("adb-prompt").innerHTML = alternatives[choice - 1].innerHTML;
    }
})();
</script>"""
CLOZE = re.compile(r"\{\{c([1-9]\d*)::([^{}]+?)\}\}")
IMAGE = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
AUDIO = {".mp3", ".ogg", ".wav", ".m4a"}


def require_text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} needs nonempty text")
    if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", value):
        raise ValueError(f"{label} contains a control character")
    return value.strip()


def check_keys(obj, allowed, label):
    if not isinstance(obj, dict):
        raise ValueError(f"{label} must be an object")
    unknown = obj.keys() - set(allowed)
    if unknown:
        raise ValueError(f"{label}: unknown fields {sorted(unknown)}")


def strings(value, label):
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array")
    return [require_text(item, label) for item in value]


def rendered(value):
    return "<br>".join(html.escape(value, quote=False).splitlines())


def cloze_count(text):
    matches = list(CLOZE.finditer(text))
    remainder = CLOZE.sub("", text)
    if not matches or re.search(r"\{\{c|\}\}", remainder, re.I):
        raise ValueError("expected complete, non-nested {{c1::answer}} deletions")
    for match in matches:
        if not match[2].partition("::")[0].strip() or int(match[1]) > 500:
            raise ValueError("cloze needs a visible answer and an index from 1 to 500")
    return len({m[1] for m in matches})


def attachment(name, base, stage):
    if stage is None:
        raise ValueError("media attachments require .apkg output")
    path = (base / name).resolve()
    if not path.is_relative_to(base) or not path.is_file():
        raise ValueError(f"missing or outside the manifest directory: {name}")
    suffix = path.suffix.lower()
    if suffix not in IMAGE | AUDIO:
        raise ValueError(f"unsupported media extension {suffix!r}")
    data = path.read_bytes()
    if not data:
        raise ValueError(f"empty media file: {name}")
    filename = f"adb-{hashlib.sha256(data).hexdigest()[:24]}{suffix}"
    target = stage / filename
    if not target.exists():
        target.write_bytes(data)
    return f'<img src="{filename}">' if suffix in IMAGE else f"[sound:{filename}]"


def parse_note(note, base, stage):
    if not isinstance(note, dict):
        raise ValueError("expected an object")
    key = require_text(note.get("id"), "id")
    kind = require_text(note.get("type"), "type")
    if kind not in MODELS:
        raise ValueError(f"unknown note type {kind!r}")
    a, b = ("text", "extra") if kind == "cloze" else ("front", "back")
    allowed = ["id", "type", a, b, "tags", "front_media", "back_media"]
    if kind == "varied":
        allowed.append("variants")
    check_keys(note, allowed, key)
    first = require_text(note.get(a), a)
    second = note.get(b, "")
    if kind != "cloze" or second != "":
        second = require_text(second, b)
    count = cloze_count(first) if kind == "cloze" else 1 + (kind == "reversed")
    tags = strings(note.get("tags", []), "tags")
    if any(re.search(r"\s", tag) for tag in tags):
        raise ValueError("each tag must be one token")
    fields = [rendered(first), rendered(second)]
    if kind == "varied":
        variants = strings(note.get("variants"), "variants")
        if not variants:
            raise ValueError("varied notes need at least one alternate prompt")
        cues = [unicodedata.normalize("NFC", " ".join(c.split())).casefold() for c in [first, *variants]]
        if len(set(cues)) != len(cues):
            raise ValueError("each alternate prompt must be distinct")
        fields.extend(["".join(f"<div>{rendered(v)}</div>" for v in variants), ""])
    front_index = 3 if kind == "varied" else 0
    for idx, side in [(front_index, "front_media"), (1, "back_media")]:
        for name in strings(note.get(side, []), side):
            fields[idx] += "<br>" + attachment(name, base, stage)
    return key, kind, fields, tags, count


def package_guid(namespace, key):
    try:
        import genanki
    except ImportError as exc:
        raise ValueError("package-compatible export requires genanki==0.13.1") from exc
    return genanki.guid_for(json.dumps([namespace, key], ensure_ascii=False))


def write_tsv(path, deck, namespace, rows):
    with path.open("w", encoding="utf-8", newline="") as out:
        uses_custom_model = any(kind == "varied" for _, kind, _, _, _ in rows)
        width = max(len(fields) for _, _, fields, _, _ in rows)
        out.write(f"#separator:Tab\n#html:true\n#notetype column:1\n#deck column:2\n#tags column:{width + 3}\n")
        if uses_custom_model:
            out.write(f"#guid column:{width + 4}\n")
        writer = csv.writer(out, delimiter="\t", lineterminator="\n")
        for key, kind, fields, tags, _ in rows:
            model_name = MODELS[kind]
            if uses_custom_model and kind != "varied":
                # Mixed exports accompany a package that installs genanki's named models.
                model_name += " (genanki)"
            padding = [""] * (width - len(fields))
            columns = [model_name, deck, *fields, *padding, " ".join(tags)]
            if uses_custom_model:
                columns.append(package_guid(namespace, key))
            writer.writerow(columns)


def write_package(path, deck_name, namespace, rows, media):
    try:
        import genanki
    except ImportError as exc:
        raise ValueError("package export requires genanki==0.13.1 (see SKILL.md)") from exc
    models = {"basic": genanki.BASIC_MODEL, "reversed": genanki.BASIC_AND_REVERSED_CARD_MODEL,
              "cloze": genanki.CLOZE_MODEL}
    if any(kind == "varied" for _, kind, _, _, _ in rows):
        models["varied"] = genanki.Model(
            1743920214, MODELS["varied"],
            fields=[{"name": name} for name in ("Front", "Back", "Alternatives", "PromptMedia")],
            templates=[{"name": "Recall", "qfmt": VARIED_FRONT, "afmt": "{{Back}}"}],
            css=".card { font: 20px/1.5 sans-serif; text-align: left; } [hidden] { display: none; }",
        )
    digest = hashlib.sha256(("anki-deck-builder/" + namespace).encode()).digest()
    deck = genanki.Deck(1_000_000_000 + int.from_bytes(digest[:6], "big"), deck_name)
    for pos, (key, kind, fields, tags, _) in enumerate(rows, start=1):
        guid = package_guid(namespace, key)
        deck.add_note(genanki.Note(model=models[kind], fields=fields, tags=tags, guid=guid, due=pos))
    # genanki creates an intermediate SQLite database via tempfile.mkstemp().
    previous = tempfile.tempdir
    try:
        tempfile.tempdir = str(media.parent)
        genanki.Package(deck, media_files=sorted(media.iterdir())).write_to_file(path)
    finally:
        tempfile.tempdir = previous


def build(source, destination):
    suffix = destination.suffix.lower()
    if suffix not in {".apkg", ".tsv"} or source.resolve() == destination.resolve():
        raise ValueError("provide a separate output file ending in .apkg or .tsv")
    doc = json.loads(source.read_text(encoding="utf-8-sig"))
    check_keys(doc, ["deck", "namespace", "notes"], "manifest")
    deck = require_text(doc.get("deck"), "deck")
    namespace = require_text(doc.get("namespace"), "namespace")
    if re.search(r"[\t\r\n]", deck) or any(not part.strip() for part in deck.split("::")):
        raise ValueError("deck must have a single-line name with nonempty hierarchy components")
    if not isinstance(doc.get("notes"), list) or not doc["notes"]:
        raise ValueError("notes must be a nonempty array")

    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as work:
        stage = Path(work).resolve()
        media = stage / "media"
        media.mkdir()
        rows, seen_ids, seen_prompts = [], set(), set()
        for idx, note in enumerate(doc["notes"], start=1):
            try:
                row = parse_note(note, source.resolve().parent, media if suffix == ".apkg" else None)
                key, kind, fields, _, _ = row
                cue = unicodedata.normalize("NFC", " ".join(fields[0].split())).casefold()
                if key in seen_ids or (kind, cue) in seen_prompts:
                    raise ValueError(f"repeated ID or cue at {key!r}; merge or disambiguate")
                seen_ids.add(key)
                seen_prompts.add((kind, cue))
                rows.append(row)
            except ValueError as exc:
                raise ValueError(f"note {idx}: {exc}") from exc
        pending = stage / ("deck" + suffix)
        if suffix == ".apkg":
            write_package(pending, deck, namespace, rows, media)
        else:
            write_tsv(pending, deck, namespace, rows)
        pending.replace(destination)
    print(f"{destination}: {len(rows)} notes, {sum(row[-1] for row in rows)} cards")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    try:
        build(args.manifest, args.output)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"build_deck: {exc}\n")


if __name__ == "__main__":
    main()
