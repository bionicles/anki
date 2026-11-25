"""Build the illustrated Series 65 package or verify its Anki import and editable export."""
import argparse
import csv
import html
import json
from pathlib import Path
import sys
import tempfile

import genanki

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent))
from finance_media import apply_figure, read_figures

SPEC = json.loads((ROOT/"model.json").read_text())
FIELDS = SPEC["fields"]
MODEL = genanki.Model(SPEC["model_id"],SPEC["model_name"],fields=[{"name":k} for k in FIELDS],
                      templates=SPEC["templates"],css=SPEC["css"])


def contents():
    figures = read_figures(ROOT)
    with (ROOT/"cards.tsv").open(newline="",encoding="utf-8") as f:
        cards=list(csv.DictReader(f,delimiter="\t"))
    keys={r["CardID"] for r in cards}
    if len(keys)!=len(cards) or len({r["GUID"] for r in cards})!=len(cards) or figures.keys()-keys:
        raise ValueError("Duplicate identity or unknown visual card ID")
    with (ROOT/"coverage.csv").open(newline="",encoding="utf-8") as f:
        if {r["card_id"] for r in csv.DictReader(f)}!=keys:
            raise ValueError("Outline map and card IDs differ")
    notes=[]
    for r in cards:
        fields={k:html.escape(r[k],quote=False) for k in FIELDS}
        tags=apply_figure(fields,r["Tags"],figures.get(r["CardID"]))
        notes.append([r["GUID"],*[fields[k] for k in FIELDS],tags])
    media={ROOT/"media"/r["Filename"] for r in figures.values()}
    return notes, media


def build(path,notes,media):
    if path.exists(): raise ValueError("Choose a fresh build directory")
    with tempfile.TemporaryDirectory(dir=path.parent) as stage:
        out=Path(stage)/"out"
        out.mkdir()
        deck=genanki.Deck(SPEC["deck_id"],SPEC["deck_name"])
        for due,(guid,*fields,tags) in enumerate(notes,1):
            deck.add_note(genanki.Note(model=MODEL,fields=fields,guid=guid,tags=tags.split(),due=due))
        genanki.Package(deck,media_files=[str(p) for p in sorted(media)]).write_to_file(out/"Series-65.apkg")
        with (out/"Series-65.tsv").open("w",newline="",encoding="utf-8") as f:
            f.write(f"#separator:Tab\n#html:true\n#notetype:{MODEL.name}\n#deck:{SPEC['deck_name']}\n"
                    f"#guid column:1\n#tags column:{len(FIELDS)+2}\n#columns:")
            w=csv.writer(f,delimiter="\t",lineterminator="\n")
            w.writerow(["GUID",*FIELDS,"Tags"])
            csv.writer(f,delimiter="\t",quoting=csv.QUOTE_ALL,lineterminator="\n").writerows(notes)
        out.rename(path)


def verify(path,notes,media):
    from anki.collection import Collection
    from anki.import_export_pb2 import ImportAnkiPackageRequest, ImportCsvRequest
    path=path.resolve()
    with (path/"Series-65.tsv").open(newline="",encoding="utf-8") as f:
        # Skip only Anki directives. A valid Anki GUID can begin with '#'.
        for line in f:
            if line.startswith("#columns:"): break
        assert list(csv.reader(f,delimiter="\t"))==notes
    expected={g:(fs,set(tags.split())) for g,*fs,tags in notes}
    with tempfile.TemporaryDirectory() as tmp:
        col=Collection(str(Path(tmp)/"check.anki2"))
        try:
            col.import_anki_package(ImportAnkiPackageRequest(package_path=str(path/"Series-65.apkg")))
            def snapshot():
                result={}
                for cid in col.find_cards(""):
                    card=col.get_card(cid);note=card.note()
                    fields,tags=expected[note.guid]
                    assert note.fields==fields and set(note.tags)==tags
                    assert note.mid==MODEL.model_id and col.decks.name(card.did)==SPEC["deck_name"]
                    assert note["Answer"] in card.answer() and note["Question"] in card.question()
                    assert ("<img" in card.question())==("visual::question" in tags)
                    assert ("<img" in card.answer())==("medium::figure" in tags)
                    assert note.guid not in result
                    result[note.guid]=(note.id,cid)
                assert result.keys()==expected.keys()
                return result
            before=snapshot()
            for p in media: assert (Path(col.media.dir())/p.name).read_bytes()==p.read_bytes()
            assert not col.media.check().missing
            for nid,_ in before.values():
                note=col.get_note(nid);note["Answer"]+=" [test edit]";col.update_note(note)
            tsv=str(path/"Series-65.tsv")
            result=col.import_csv(ImportCsvRequest(path=tsv,metadata=col.get_csv_metadata(tsv,None)))
            assert len(result.log.updated)==len(notes) and snapshot()==before
        finally:
            col.close()
    print(f"Verified {len(notes)} cards, {len(media)} figures and the Anki TSV update.")

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=["build","verify"])
    parser.add_argument("directory",type=Path)
    args=parser.parse_args()
    (build if args.action=="build" else verify)(args.directory,*contents())
