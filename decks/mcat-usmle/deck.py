"""Build, check, or refresh the combined course. All imports use a disposable Anki profile."""
import argparse
from collections import Counter, defaultdict
from contextlib import closing
import csv
import fcntl
import gzip
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import tempfile
from zipfile import ZIP_DEFLATED, ZipFile

from step_coverage import STEPS, display, measure, measure_item_depth, measure_system_depth
from extract import ROOT, FIELDS, cohort, openstax, read

RELEASE = ROOT / "release"
NAME = "MCAT and USMLE"
FILE = "MCAT-USMLE"
MODELFIELDS = ["CardID","Question","Choices","Answer","Explanation","Source","License","Figure"]
IMAGE_SUFFIXES = (".png", ".jpg", ".webp")
MEDIA_SUFFIXES = {*IMAGE_SUFFIXES, ".wav"}
EXAMS = {"MCAT","USMLE Step 1","USMLE Step 2 CK","USMLE Step 3"}


def write_table(path, columns, rows):
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def table(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def legacy_id(text):
    return 1_000_000_000 + int.from_bytes(hashlib.sha256(("mcat-usmle/"+text).encode()).digest()[:5], "big")


def label(tag):
    return re.sub(r"[^\w-]+","_",tag.strip()).strip("_")


def package_model():
    import genanki
    return genanki.Model(legacy_id("recall-v1"),"MCAT and USMLE · Clinical and science recall",
        fields=[{"name":k} for k in MODELFIELDS],
        templates=[{"name":"Recall","qfmt":"{{Question}}{{Figure}}{{Choices}}",
                    "afmt":"{{FrontSide}}<hr id=answer><b>{{Answer}}</b>{{#Explanation}}<p>{{Explanation}}</p>{{/Explanation}}<footer>{{Source}}<br>{{License}}</footer>"}],
        css=".card{font:20px/1.45 sans-serif;text-align:left;max-width:42rem;margin:auto;padding:1rem} ol{padding-left:2em} img{max-width:100%;height:auto} footer{font-size:.7em;margin-top:1em;opacity:.8}")


def remote(cfg):
    return f"https://github.com/{cfg['repo']}.git"


def head(cfg):
    out = subprocess.check_output(["git","ls-remote","--exit-code",remote(cfg),"refs/heads/"+cfg["branch"]], text=True)
    return out.split()[0]


def checkout(cfg, sha, path):
    subprocess.run(["git","init","-q",str(path)],check=True)
    def git(*args):
        subprocess.run(["git","-C",str(path),*args],check=True)
    git("remote","add","origin",remote(cfg))
    git("config","remote.origin.promisor","true")
    git("config","remote.origin.partialclonefilter","blob:none")
    git("sparse-checkout","init","--no-cone")
    patterns = ["/open-content/usmle/step1/","/open-content/modules/","/LICENSE-CONTENT.md"] if cfg["format"]=="cohort" else ["/collections/","/modules/*/index.cnxml","/LICENSE"]
    git("sparse-checkout","set","--no-cone",*patterns)
    git("fetch","-q","--no-tags","--depth=1","--filter=blob:none","origin",sha)
    git("checkout","-q","--detach","FETCH_HEAD")


def lineage(key):
    """Cohort appends a content version to an otherwise stable item identifier."""
    if key.startswith(("bank:", "cohort:")):
        return re.sub(r":v[0-9]+$", ":v1", key)
    return key


def deduplicate(rows, prior):
    """Retain a published identity when overlapping sources change or drop one copy."""
    groups = defaultdict(list)
    by_id = {}
    families = set()
    published = {lineage(src): canonical for src, canonical in prior.items()}
    for r in rows:
        if set(r)!=set(FIELDS) or r["Exam"] not in EXAMS or not all(r[k].strip() for k in ("ID","Prompt","Answer","Topic","Section","Source","License")):
            raise ValueError(f"Incomplete source note: {r.get('ID')}")
        if r["ID"] in by_id:
            raise ValueError("Repeated upstream ID: "+r["ID"])
        family = lineage(r["ID"])
        if family in families:
            raise ValueError("Multiple active revisions of one upstream item: "+family)
        families.add(family)
        by_id[r["ID"]]=r
        normalize = lambda s: " ".join(s.casefold().split())
        fingerprint = (r["Exam"],normalize(r["Prompt"]),tuple(sorted(normalize(x) for x in r["Choices"].splitlines())),r["Figure"])
        groups[fingerprint].append(r)
    output=[]; aliases={}
    used=set()
    for members in sorted(groups.values(),key=lambda group:min(x["ID"] for x in group)):
        members.sort(key=lambda r:r["ID"])
        if len({r["Answer"].casefold().strip() for r in members})!=1:
            raise ValueError("Conflicting answer keys: "+str([r["ID"] for r in members]))
        ids={r["ID"] for r in members}
        candidates = [published[lineage(key)] for key in sorted(ids) if lineage(key) in published]
        member_families = {lineage(key) for key in ids}
        old = [key for key in candidates if key not in used and
               (lineage(key) not in families or lineage(key) in member_families)]
        key=old[0] if old else next(lineage(r["ID"]) for r in members if lineage(r["ID"]) not in used)
        row=next((r for r in members if r["ID"]==key),members[0]).copy()
        row["ID"]=key;used.add(key);output.append(row)
        aliases.update({i:key for i in ids})
    return sorted(output,key=lambda r:(r["Exam"],r["Section"],r["ID"])),aliases


def render(row):
    def fmt(s):
        return html.escape(s,quote=False).replace("\n","<br>")
    options=row["Choices"].splitlines()
    choices='<ol type="A">'+"".join("<li>"+fmt(x)+"</li>" for x in options)+"</ol>" if options else ""
    fig=row["Figure"]
    if fig and (Path(fig).name!=fig or not (ROOT/"media"/fig).is_file()):
        raise ValueError("Unknown figure: "+fig)
    media_html = ""
    if fig:
        if fig.endswith(".wav"):
            media_html = "[sound:" + fig + "]"
        elif fig.endswith(IMAGE_SUFFIXES):
            media_html = '<div><img src="' + html.escape(fig, quote=True) + '"></div>'
        else:
            raise ValueError("Unsupported question media: " + fig)
    return [row["ID"],fmt(row["Prompt"]),choices,fmt(row["Answer"]),fmt(row["Reason"]),fmt(row["Source"]),fmt(row["License"]),
            media_html]


def records(folder):
    blobs=read(folder/"sources.lock.json")
    upstream=[]
    for source,info in sorted(blobs.items()):
        file=folder/(source+".json.gz")
        payload=gzip.decompress(file.read_bytes())
        if hashlib.sha256(payload).hexdigest()!=info["sha256"]:
            raise ValueError(f"Snapshot checksum mismatch: {source}")
        items=json.loads(payload)
        if len(items)!=info["notes"]:raise ValueError(f"Snapshot count mismatch: {source}")
        upstream.extend(items)
    return upstream+table(ROOT/"originals.tsv")


def alias_map(folder):
    file=folder/"aliases.tsv"
    return {r["SourceID"]:r["CardID"] for r in table(file)} if file.exists() else {}


MCAT_SCIENCE_SKILLS = {
    "Scientific knowledge": "Knowledge",
    "Scientific problem solving": "ProblemSolving",
    "Research design": "ResearchDesign",
    "Data and statistics": "DataInterpretation",
}


MCAT_CARS_SKILLS = {
    "CARS comprehension": "Comprehension",
    "CARS reasoning within a text": "WithinText",
    "CARS reasoning beyond a text": "BeyondText",
}


def reasoning_inventory(blueprint, skills):
    rows = {r["Domain"]: set(r["ReviewedCardIDs"].split()) for r in blueprint
            if r["Exam"] == "MCAT" and r["Axis"] == "Reasoning" and r["Domain"] in skills}
    if rows.keys() != skills.keys():
        raise ValueError(f"Missing MCAT reasoning rows: {sorted(skills.keys() - rows.keys())}")
    return {column: rows[skill] for skill, column in skills.items()}


def reasoning_evidence(card_ids, inventory):
    result = {}
    classified = set()
    for column, skill_ids in inventory.items():
        matches = card_ids & skill_ids
        classified.update(matches)
        result[column + "Cards"] = str(len(matches))
        result[column + "IDs"] = " ".join(sorted(matches))
    result["UnclassifiedIDs"] = " ".join(sorted(card_ids - classified))
    return result


def mcat_science_coverage(blueprint, cards=(), transfers=()):
    """Cross-reference reviewed topics, skills and independently authored changed cases."""
    inventory = reasoning_inventory(blueprint, MCAT_SCIENCE_SKILLS)
    topics = {r["Domain"]: r for r in blueprint if r["Exam"] == "MCAT" and r["Axis"] == "Subtopic"}
    topic_ids = {name: set(row["ReviewedCardIDs"].split()) for name, row in topics.items()}
    card_by_id = {card["ID"]: card for card in cards if card["Exam"] == "MCAT"}
    pairs = defaultdict(dict)
    for row in transfers:
        topic, skill = row["Subtopic"], row["Skill"]
        first, second = row["FirstID"], row["TransferID"]
        column = MCAT_SCIENCE_SKILLS.get(skill)
        ids = frozenset((first, second))
        if (len(ids) != 2 or not row["Decision"].strip() or not row["ChangedEvidence"].strip()
                or not column or not ids <= (topic_ids.get(topic, set()) & inventory[column] & card_by_id.keys())):
            raise ValueError(f"Invalid MCAT transfer evidence for {topic}, {skill}: {first}, {second}")
        group = pairs[topic, column]
        a, b = card_by_id[first], card_by_id[second]
        def normalized(value):
            return " ".join(value.split()).casefold()
        passage = normalized(a["Prompt"].rpartition("\n\n")[0])
        if (ids in group or normalized(a["Prompt"]) == normalized(b["Prompt"])
                or (a["Figure"] and a["Figure"] == b["Figure"])
                or (passage and passage == normalized(b["Prompt"].rpartition("\n\n")[0]))):
            raise ValueError(f"Repeated MCAT transfer evidence: {first}, {second}")
        group[ids] = f"{first} {second}"

    report = []
    for name, row in topics.items():
        result = dict(Subtopic=name, Outline=row["Outline"], MappedCards=str(len(topic_ids[name])))
        result.update(reasoning_evidence(topic_ids[name], inventory))
        for column in inventory:
            group = pairs[name, column]
            result[column + "Pairs"] = str(len(group))
            result[column + "PairIDs"] = " | ".join(group.values())
        result["NextAudit"] = row["NextAudit"]
        report.append(result)
    return report


def mcat_detail_coverage(blueprint, science):
    """Credit an outline detail only for reviewed IDs and complete same-category case pairs."""
    pairs = defaultdict(set)
    categories = {row["Subtopic"].partition(" · ")[0] for row in science}
    for row in science:
        category = row["Subtopic"].partition(" · ")[0]
        for column in MCAT_SCIENCE_SKILLS.values():
            for pair in row[column + "PairIDs"].split(" | "):
                if pair:
                    pairs[category].add(pair)
    report = []
    for row in blueprint:
        if (row["Exam"], row["Axis"]) != ("MCAT", "Outline detail"):
            continue
        category, _, detail = row["Domain"].partition(" · ")
        if category not in categories or not detail:
            raise ValueError(f"Unknown category or empty MCAT detail: {row['Domain']}")
        ids = set(row["ReviewedCardIDs"].split())
        matched = sorted(pair for pair in pairs[category] if set(pair.split()) <= ids)
        report.append(dict(Category=category, Detail=detail, Outline=row["Outline"],
                           MappedCards=str(len(ids)), CardIDs=" ".join(sorted(ids)),
                           ChangedPairs=str(len(matched)), PairIDs=" | ".join(matched),
                           NextAudit=row["NextAudit"]))
    return report


def reviewed_mcat_science(cards, blueprint):
    return mcat_science_coverage(blueprint, cards, table(ROOT/"mcat-transfer.tsv"))


def mcat_cars_coverage(cards, blueprint):
    """Count distinct passage text once, regardless of how many questions repeat it."""
    inventory = reasoning_inventory(blueprint, MCAT_CARS_SKILLS)
    passages = defaultdict(list)
    for card in cards:
        if card["Exam"] == "MCAT" and card["Section"] == "Critical Analysis and Reasoning Skills":
            passage, _, _ = card["Prompt"].rpartition("\n\n")
            passages[passage.strip()].append(card)
    report = []
    for passage, questions in passages.items():
        ids = {card["ID"] for card in questions}
        topics = sorted({card["Topic"] for card in questions})
        name = " | ".join(topics) if passage else "No passage text identified"
        result = dict(Passage=name, PassageWords=str(len(passage.split())),
                      Questions=str(len(ids)), QuestionIDs=" ".join(sorted(ids)))
        result.update(reasoning_evidence(ids, inventory))
        report.append(result)
    return sorted(report, key=lambda r: (r["Passage"], r["QuestionIDs"]))


def step_measurements(cards):
    return measure(table(ROOT/"step-families.tsv"), table(ROOT/"blueprint.tsv"),
                   table(ROOT/"step-depth.tsv"), table(ROOT/"step-weights.tsv"), cards, table(ROOT/"step-items.tsv"))


def named_measurements():
    return measure_item_depth(table(ROOT/"step-families.tsv"), table(ROOT/"step-items.tsv"),
                              table(ROOT/"step-depth.tsv"))


def make(folder, prior):
    import genanki
    model=package_model()
    rows,aliases=deduplicate(records(folder),prior)
    write_table(folder/"aliases.tsv",["SourceID","CardID"],[{"SourceID":s,"CardID":c} for s,c in sorted(aliases.items())])
    old_retired={r["CardID"] for r in table(RELEASE/"retired.tsv")} if (RELEASE/"retired.tsv").exists() else set()
    retired=(old_retired|set(prior.values()))-set(aliases.values())
    write_table(folder/"retired.tsv",["CardID"],[{"CardID":k} for k in sorted(retired)])
    report, practice_tags = step_measurements(rows)
    write_table(folder/"step-coverage.tsv", list(report[0]), report)
    blueprint = table(ROOT/"blueprint.tsv")
    cars = mcat_cars_coverage(rows, blueprint)
    write_table(folder/"mcat-cars-coverage.tsv", list(cars[0]), cars)
    science = reviewed_mcat_science(rows, blueprint)
    write_table(folder/"mcat-science-coverage.tsv", list(science[0]), science)
    details = mcat_detail_coverage(blueprint, science)
    write_table(folder/"mcat-outline-details.tsv", list(details[0]), details)
    named = named_measurements()
    write_table(folder/"step-item-coverage.tsv", list(named[0]), named)
    systems = measure_system_depth(named)
    write_table(folder/"step-system-coverage.tsv", list(systems[0]), systems)
    decks={}; media=set(); objectives=defaultdict(list)
    with (folder/(FILE+".tsv")).open("w",newline="",encoding="utf-8") as f:
        f.write(f"#separator:Tab\n#html:true\n#notetype:{model.name}\n#deck column:2\n#guid column:1\n#tags column:11\n#columns:")
        w=csv.writer(f,delimiter="\t",lineterminator="\n",quoting=csv.QUOTE_MINIMAL)
        w.writerow(["GUID","Deck",*MODELFIELDS,"Tags"])
        w=csv.writer(f,delimiter="\t",lineterminator="\n",quoting=csv.QUOTE_ALL)
        for n,r in enumerate(rows,1):
            name="::".join([NAME,r["Exam"],r["Section"]])
            if name not in decks:decks[name]=genanki.Deck(legacy_id(name),name)
            source=r["ID"].split(":")[0]
            source="cohort" if source in {"bank","cohort"} else source
            tags=["exam::"+label(r["Exam"]),"section::"+label(r["Section"]),"topic::"+label(r["Topic"]),"source::"+label(source)]
            if r["Figure"]:
                media.add(str(ROOT/"media"/r["Figure"]))
                tags.append("listening::question" if r["Figure"].endswith(".wav") else "visual::question")
            tags.extend(sorted(practice_tags[r["ID"]]))
            fields=render(r);guid=genanki.guid_for("mcat-usmle/v1",r["ID"])
            decks[name].add_note(genanki.Note(model=model,fields=fields,guid=guid,tags=tags,due=n))
            w.writerow([guid,name,*fields," ".join(tags)])
            objectives[r["Exam"],r["Section"],r["Topic"]].append(r["ID"])
    write_table(folder/"coverage.tsv",["Exam","Section","Topic","Cards","CardIDs"],
                [dict(Exam=e,Section=s,Topic=t,Cards=len(ids),CardIDs=" ".join(ids))
                 for (e,s,t),ids in sorted(objectives.items())])
    # genanki stores every member uncompressed, including the Anki database and audio.
    package = genanki.Package(list(decks.values()), media_files=sorted(media))
    with tempfile.TemporaryFile() as raw:
        package.write_to_file(raw)
        with ZipFile(raw) as source, ZipFile(folder / (FILE + ".apkg"), "w", ZIP_DEFLATED) as output:
            # Longer notes and passages span fewer SQLite pages at this size.
            # Repack the generated database before ZIP compression.
            with tempfile.TemporaryDirectory() as scratch:
                db_path = source.extract("collection.anki2", scratch)
                with closing(sqlite3.connect(db_path)) as database:
                    database.execute("PRAGMA page_size = 16384")
                    database.execute("VACUUM")
                output.write(db_path, "collection.anki2", compresslevel=9)
            for name in source.namelist():
                if name == "collection.anki2":
                    continue
                with source.open(name) as entry, output.open(name, "w") as target:
                    shutil.copyfileobj(entry, target)
    return rows


def verify_imaging(cards):
    images = table(ROOT / "imaging.tsv")
    credits = {row["Figure"]: row for row in images}
    assert len(credits) == len(images)
    assert set(credits) == {p.name for p in (ROOT / "media").glob("med_rad_*")}
    for row in images:
        assert re.fullmatch(r"[0-9a-f]{40}", row["SourceSHA1"]), row
        assert (row["Source"].startswith("https://commons.wikimedia.org/wiki/File:")
                or re.fullmatch(r"https://pmc\.ncbi\.nlm\.nih\.gov/articles/PMC[0-9]+/#(?:F(?:IG)?[0-9]+|[a-zA-Z][a-zA-Z0-9_-]*-fig-[0-9]+)", row["Source"])), row
        assert row["LicenseURL"].startswith("https://creativecommons.org/"), row
    for card in cards:
        if card["Figure"] in credits:
            credit = credits[card["Figure"]]
            assert credit["Source"] in card["Source"], card["ID"]
            assert all(credit[k] and credit[k] in card["License"]
                       for k in ("Creator", "License", "LicenseURL")), card["ID"]


def verify_ptbxl(cards):
    records = table(ROOT / "ptbxl.tsv")
    credits = {row["Figure"]: row for row in records}
    assert len(credits) == len(records)
    assert set(credits) == {p.name for p in (ROOT / "media").glob("med_ptbxl_*.png")}
    used = set()
    for card in cards:
        figure = card["Figure"]
        if figure in credits:
            row = credits[figure]
            assert row["Record"] in card["Source"] and "10.13026/kfzx-aw45" in card["Source"]
            assert "https://creativecommons.org/licenses/by/4.0/" in card["License"]
            used.add(figure)
    assert used == set(credits)


def verify(folder):
    import genanki
    from anki.collection import Collection
    from anki.import_export_pb2 import ImportAnkiPackageRequest, ImportCsvRequest
    expected,aliases=deduplicate(records(folder),alias_map(folder))
    assert aliases==alias_map(folder)
    assert {r["Exam"] for r in expected}==EXAMS
    keyed={r["ID"]:r for r in expected}
    assert set(read(folder/"sources.lock.json")) == {c["id"] for c in read(ROOT/"sources.json")}
    categories = {r["Topic"].partition(" ")[0] for r in expected if r["Exam"]=="MCAT"}
    assert set("1A 1B 1C 1D 2A 2B 2C 3A 3B 4A 4B 4C 4D 4E 5A 5B 5C 5D 5E 6A 6B 6C 7A 7B 7C 8A 8B 8C 9A 9B 10A".split()) <= categories
    assert len({r["Section"] for r in expected if r["Exam"]=="MCAT"})==4
    assert {r["Section"] for r in expected if r["Exam"]=="USMLE Step 3"}=={"CCS Cases","Foundations of Independent Practice","Advanced Clinical Medicine"}
    blueprint=table(ROOT/"blueprint.tsv")
    assert {r["Exam"] for r in blueprint} == EXAMS
    assert len({(r["Exam"],r["Axis"],r["Domain"]) for r in blueprint})==len(blueprint)
    for row in blueprint:
        ids=row["ReviewedCardIDs"].split()
        assert row["Outline"].startswith("https://") and row["NextAudit"]
        assert row["Status"] in {"Partial","Unmapped","Verified"}
        assert bool(ids)==(row["Status"]!="Unmapped")
        assert all(k in keyed and keyed[k]["Exam"]==row["Exam"] for k in ids), row
    science = reviewed_mcat_science(expected, blueprint)
    assert table(folder/"mcat-science-coverage.tsv") == science
    assert table(folder/"mcat-outline-details.tsv") == mcat_detail_coverage(blueprint, science)
    assert table(folder/"mcat-cars-coverage.tsv") == mcat_cars_coverage(expected, blueprint)
    report, practice_tags = step_measurements(expected)
    assert table(folder/"step-coverage.tsv") == report
    named = named_measurements()
    assert table(folder/"step-item-coverage.tsv") == named
    assert table(folder/"step-system-coverage.tsv") == measure_system_depth(named)
    assert {r["Family"] for r in table(ROOT/"step-families.tsv")} == {r["Family"] for r in table(ROOT/"step-items.tsv")}, "A Step family is missing from the named-topic inventory"
    verify_imaging(expected)
    verify_ptbxl(expected)
    sound_records = table(ROOT/"heart-sounds.tsv")
    clips = {r["Clip"]: r for r in sound_records}
    assert len(clips) == len(sound_records)
    assert set(clips) == {p.stem for p in (ROOT/"media").glob("*.wav")}
    for card in expected:
        stem = Path(card["Figure"]).stem
        if stem in clips:
            assert clips[stem]["Record"] in card["Source"] and "ODC-By 1.0" in card["License"], card["ID"]
    coverage=table(folder/"coverage.tsv")
    mapped=[]
    for row in coverage:
        ids=row["CardIDs"].split()
        assert len(ids)==int(row["Cards"]) and all(all(row[k]==keyed[i][k] for k in ("Exam","Topic","Section")) for i in ids)
        mapped.extend(ids)
    assert Counter(mapped)==Counter(keyed.keys())
    assert {r["Figure"] for r in expected if r["Figure"]}=={p.name for p in (ROOT/"media").iterdir() if p.suffix in MEDIA_SUFFIXES}
    tsv=folder/(FILE+".tsv")
    with tsv.open(newline="") as f:
        for line in f:
            if line.startswith("#columns:"):break
        export={r[2]:r for r in csv.reader(f,delimiter="\t")}
    with tempfile.TemporaryDirectory() as d:
        col=Collection(str(Path(d)/"review.anki2"))
        try:
            col.import_anki_package(ImportAnkiPackageRequest(package_path=str((folder/(FILE+".apkg")).resolve())))
            def snapshot():
                result={}
                for cid in col.find_cards(""):
                    c=col.get_card(cid);n=c.note();key=n["CardID"];r=keyed[key];fields=render(r)
                    assert n.fields==fields and n.guid==genanki.guid_for("mcat-usmle/v1",key)
                    assert col.decks.name(c.did)=="::".join([NAME,r["Exam"],r["Section"]])
                    assert export[key]==[n.guid,col.decks.name(c.did),*fields,export[key][-1]]
                    assert {t.casefold() for t in n.tags}=={t.casefold() for t in export[key][-1].split()}, (key,n.tags,export[key][-1])
                    assert practice_tags[key] == {t for t in n.tags if t.startswith(("outline::", "practice::"))}
                    assert n["Question"] in c.question() and n["Answer"] in c.answer(), (key,n["Answer"],c.answer()[:500])
                    if r["Figure"].endswith(".wav"):
                        assert [t.filename for t in c.question_av_tags()] == [r["Figure"]], key
                    assert key not in result;result[key]=(n.id,cid)
                assert result.keys()==keyed.keys()==export.keys()
                return result
            ids=snapshot()
            for nid,_ in ids.values():
                n=col.get_note(nid);n["Answer"]+=" [test]";col.update_note(n)
            result=col.import_csv(ImportCsvRequest(path=str(tsv.resolve()),metadata=col.get_csv_metadata(str(tsv.resolve()),None)))
            assert len(result.log.updated)==len(expected) and snapshot()==ids
            for filename in {r["Figure"] for r in expected if r["Figure"]}:
                assert (ROOT/"media"/filename).read_bytes()==(Path(col.media.dir())/filename).read_bytes()
            assert not col.media.check().missing
        finally:col.close()
    print("Verified Anki package and editable re-import:",dict(Counter(r["Exam"] for r in expected)))


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_inputs(lock):
    paths = [ROOT / name for name in ("deck.py", "extract.py", "terms.txt", "Justfile", "originals.tsv", "sources.json", "blueprint.tsv", "mcat-transfer.tsv", "specimens.tsv", "imaging.tsv", "step-families.tsv", "step-depth.tsv", "step-weights.tsv", "step-items.tsv", "step_coverage.py", "intrapartum.py", "ptbxl.py", "ptbxl.tsv", "figures.py", "heart-sounds.tsv", "heart_sounds.py")]
    paths.extend(sorted(p for p in (ROOT / "media").iterdir() if p.suffix in MEDIA_SUFFIXES))
    return {"sources": lock, "files": {p.relative_to(ROOT).as_posix(): file_hash(p) for p in paths}}


def files_in_release(folder):
    return {p.name: file_hash(p) for p in sorted(folder.iterdir()) if p.name != "build.json"}


def current_build(folder, inputs):
    receipt = folder / "build.json"
    if not receipt.exists():
        return False
    info = read(receipt)
    return info["inputs"] == inputs and info["outputs"] == files_in_release(folder)


def display_gaps(items, science, details=()):
    """Show the largest outstanding editorial workloads, with concrete examples."""
    def show(groups):
        ranked = sorted(groups.items(), key=lambda entry: (-len(entry[1]), entry[0]))
        if not ranked:
            print("  No outstanding gaps in this band")
        for group, gaps in ranked[:3]:
            print(f"  {group} ({len(gaps)}) — " + " / ".join(sorted(gaps)[:2]))

    print("MCAT science • missing topic–skill combinations by content category")
    groups = defaultdict(list)
    for row in science:
        category, _, topic = row["Subtopic"].partition(" · ")
        for skill, column in MCAT_SCIENCE_SKILLS.items():
            if not int(row[column + "Cards"]):
                groups[category].append(f"{topic} ({skill})")
    show(groups)
    if details:
        listed = {row["Category"] for row in details}
        all_categories = {row["Subtopic"].partition(" · ")[0] for row in science}
        missing = sorted(all_categories - listed)
        print(f"MCAT outline detail inventory covers {len(listed)} of {len(all_categories)} categories")
        if missing:
            print("  Categories awaiting detailed inventory: " + ", ".join(missing))
        for field, description in (("MappedCards", "a specifically linked question"),
                                   ("ChangedPairs", "a linked changed-case pair")):
            groups = defaultdict(list)
            for row in details:
                if not int(row[field]):
                    groups[row["Category"]].append(row["Detail"])
            print(f"MCAT indexed outline details without {description}")
            show(groups)
    for exam in STEPS:
        breadth = defaultdict(list)
        depth = defaultdict(list)
        for row in items:
            if row["Exam"] != exam:
                continue
            if not int(row["MappedCards"]):
                breadth[row["Family"]].append(row["Item"])
            elif not int(row["ThreeLevelObjectives"]):
                depth[row["Family"]].append(row["Item"])
        print(f"{exam} • named topics without a linked card, by family")
        show(breadth)
        print(f"{exam} • linked topics without a three-card sequence, by family")
        show(depth)
    print("MCAT science • represented topic–skill combinations without a reviewed changed case")
    groups = defaultdict(list)
    for row in science:
        category, _, topic = row["Subtopic"].partition(" · ")
        for skill, column in MCAT_SCIENCE_SKILLS.items():
            if int(row[column + "Cards"]) and not int(row[column + "Pairs"]):
                groups[category].append(f"{topic} ({skill})")
    show(groups)

    steps_without_cards = defaultdict(set)
    for row in items:
        if not int(row["MappedCards"]):
            steps_without_cards[row["Family"], row["Item"]].add(row["Exam"])
    groups = defaultdict(list)
    all_steps = set(STEPS)
    for (family, item), missing_steps in steps_without_cards.items():
        if missing_steps == all_steps:
            groups[family].append(item)
    total = sum(len(topics) for topics in groups.values())
    print(f"Named topics without a linked card on any USMLE Step • {total}")
    show(groups)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=["check","update","build","test","coverage","gaps"])
    parser.add_argument("--checkout",action="append",default=[],metavar="ID=PATH",help="Use this local Git checkout at its HEAD for update")
    args=parser.parse_args()
    configs=read(ROOT/"sources.json")
    local={k:Path(v).resolve() for k,v in (s.split("=",1) for s in args.checkout)}
    if local.keys()-{c["id"] for c in configs}:parser.error("Unknown checkout ID")
    with (ROOT/"Justfile").open() as lock:
        fcntl.flock(lock,fcntl.LOCK_EX if args.action in {"update","build"} else fcntl.LOCK_SH)
        if args.action=="gaps":
            cards, _ = deduplicate(records(RELEASE), alias_map(RELEASE))
            blueprint = table(ROOT/"blueprint.tsv")
            science = reviewed_mcat_science(cards, blueprint)
            display_gaps(named_measurements(), science, mcat_detail_coverage(blueprint, science))
            return
        if args.action=="coverage":
            cards, _ = deduplicate(records(RELEASE), alias_map(RELEASE))
            blueprint = table(ROOT/"blueprint.tsv")
            cars = [r for r in mcat_cars_coverage(cards, blueprint) if int(r["PassageWords"])]
            print("CARS passages with reviewed evidence for each reasoning skill")
            for skill, column in MCAT_CARS_SKILLS.items():
                represented = sum(int(row[column + "Cards"]) > 0 for row in cars)
                print(f"  {skill}: {represented}/{len(cars)}")
            science = reviewed_mcat_science(cards, blueprint)
            print("MCAT science subtopics with reviewed evidence for each reasoning skill")
            for skill, column in MCAT_SCIENCE_SKILLS.items():
                represented = sum(int(row[column + "Cards"]) > 0 for row in science)
                print(f"  {skill}: {represented}/{len(science)}")
            print("MCAT science subtopics with a reviewed changed case for each reasoning skill")
            for skill, column in MCAT_SCIENCE_SKILLS.items():
                represented = sum(int(row[column + "Pairs"]) > 0 for row in science)
                print(f"  {skill}: {represented}/{len(science)}")
            details = mcat_detail_coverage(blueprint, science)
            print("MCAT detailed outline review by indexed category")
            for category in sorted({row["Category"] for row in details}):
                rows = [row for row in details if row["Category"] == category]
                linked = sum(int(row["MappedCards"]) > 0 for row in rows)
                paired = sum(int(row["ChangedPairs"]) > 0 for row in rows)
                print(f"  {category}: {len(rows)} details, {linked} linked, {paired} with changed cases")
            display(step_measurements(cards)[0], named_measurements())
            return
        if args.action=="test":verify(RELEASE);return
        previous=read(RELEASE/"sources.lock.json") if RELEASE.exists() else {}
        revisions={}
        if args.action in {"check","update"}:
            for cfg in configs:
                k=cfg["id"]
                revisions[k]=subprocess.check_output(["git","-C",str(local[k]),"rev-parse","HEAD"],text=True).strip() if k in local else head(cfg)
                old=previous.get(k,{}).get("commit","")
                print(f"{k}: {'current' if old==revisions[k] else 'update available'} {old[:10] or '(new)'} -> {revisions[k][:10]}",flush=True)
            if args.action=="check":return
        with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
            work=Path(tmp);out=work/"out";out.mkdir();newlock={}
            for cfg in configs:
                k=cfg["id"];snapshot=k+".json.gz"
                if args.action=="build":
                    shutil.copyfile(RELEASE/snapshot,out/snapshot);newlock[k]=previous[k];continue
                commit=revisions[k]
                recipe=hashlib.sha256((ROOT/"extract.py").read_bytes()+(ROOT/"terms.txt").read_bytes()+json.dumps(cfg,sort_keys=True).encode()).hexdigest()
                if previous.get(k,{}).get("commit")==commit and previous[k].get("recipe")==recipe:
                    shutil.copyfile(RELEASE/snapshot,out/snapshot);newlock[k]=previous[k];continue
                path=local.get(k)
                if path is None:
                    path=work/k;checkout(cfg,commit,path)
                elif subprocess.check_output(["git","-C",str(path),"status","--porcelain","--untracked-files=no"],text=True).strip():
                    raise ValueError("Use a clean source checkout: "+str(path))
                converter=cohort if cfg["format"]=="cohort" else openstax
                items=list(converter(path,cfg,commit))
                if not items:raise ValueError("Empty source: "+k)
                payload=json.dumps(items,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()
                (out/snapshot).write_bytes(gzip.compress(payload,mtime=0))
                newlock[k]=dict(commit=commit,repo=cfg["repo"],sha256=hashlib.sha256(payload).hexdigest(),notes=len(items),recipe=recipe)
            (out/"sources.lock.json").write_text(json.dumps(newlock,indent=2,sort_keys=True)+"\n")
            inputs=build_inputs(newlock)
            if args.action=="update" and current_build(RELEASE,inputs):
                print("Release is current. All artifact checksums match.")
                return
            make(out,alias_map(RELEASE));verify(out)
            (out/"build.json").write_text(json.dumps({"inputs":inputs,"outputs":files_in_release(out)},indent=2,sort_keys=True)+"\n")
            backup=work/"previous"
            if RELEASE.exists():RELEASE.rename(backup)
            try:out.rename(RELEASE)
            except BaseException:
                if backup.exists():backup.rename(RELEASE)
                raise


if __name__=="__main__":
    main()
