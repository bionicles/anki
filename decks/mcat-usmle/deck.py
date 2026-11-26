"""Build, check, or refresh the combined course. All imports use a disposable Anki profile."""
import argparse
from collections import Counter, defaultdict
import csv
import fcntl
import gzip
import hashlib
import html
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

from extract import ROOT, FIELDS, cohort, openstax, read

RELEASE = ROOT / "release"
NAME = "MCAT and USMLE"
FILE = "MCAT-USMLE"
MODELFIELDS = ["CardID","Question","Choices","Answer","Explanation","Source","License","Figure"]
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
    return [row["ID"],fmt(row["Prompt"]),choices,fmt(row["Answer"]),fmt(row["Reason"]),fmt(row["Source"]),fmt(row["License"]),
            '<div><img src="'+html.escape(fig,quote=True)+'"></div>' if fig else ""]


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


def make(folder, prior):
    import genanki
    model=package_model()
    rows,aliases=deduplicate(records(folder),prior)
    write_table(folder/"aliases.tsv",["SourceID","CardID"],[{"SourceID":s,"CardID":c} for s,c in sorted(aliases.items())])
    old_retired={r["CardID"] for r in table(RELEASE/"retired.tsv")} if (RELEASE/"retired.tsv").exists() else set()
    retired=(old_retired|set(prior.values()))-set(aliases.values())
    write_table(folder/"retired.tsv",["CardID"],[{"CardID":k} for k in sorted(retired)])
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
            if r["Figure"]:media.add(str(ROOT/"media"/r["Figure"]));tags.append("visual::question")
            fields=render(r);guid=genanki.guid_for("mcat-usmle/v1",r["ID"])
            decks[name].add_note(genanki.Note(model=model,fields=fields,guid=guid,tags=tags,due=n))
            w.writerow([guid,name,*fields," ".join(tags)])
            objectives[r["Exam"],r["Section"],r["Topic"]].append(r["ID"])
    write_table(folder/"coverage.tsv",["Exam","Section","Topic","Cards","CardIDs"],
                [dict(Exam=e,Section=s,Topic=t,Cards=len(ids),CardIDs=" ".join(ids))
                 for (e,s,t),ids in sorted(objectives.items())])
    genanki.Package(list(decks.values()),media_files=sorted(media)).write_to_file(folder/(FILE+".apkg"))
    return rows


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
    coverage=table(folder/"coverage.tsv")
    mapped=[]
    for row in coverage:
        ids=row["CardIDs"].split()
        assert len(ids)==int(row["Cards"]) and all(all(row[k]==keyed[i][k] for k in ("Exam","Topic","Section")) for i in ids)
        mapped.extend(ids)
    assert Counter(mapped)==Counter(keyed.keys())
    assert {r["Figure"] for r in expected if r["Figure"]}=={p.name for p in (ROOT/"media").glob("*.png")}
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
                    assert n["Question"] in c.question() and n["Answer"] in c.answer(), (key,n["Answer"],c.answer()[:500])
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
    paths = [ROOT / name for name in ("deck.py", "extract.py", "terms.txt", "Justfile", "originals.tsv", "sources.json")]
    paths.extend(sorted((ROOT / "media").glob("*.png")))
    return {"sources": lock, "files": {p.relative_to(ROOT).as_posix(): file_hash(p) for p in paths}}


def files_in_release(folder):
    return {p.name: file_hash(p) for p in sorted(folder.iterdir()) if p.name != "build.json"}


def current_build(folder, inputs):
    receipt = folder / "build.json"
    if not receipt.exists():
        return False
    info = read(receipt)
    return info["inputs"] == inputs and info["outputs"] == files_in_release(folder)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=["check","update","build","test"])
    parser.add_argument("--checkout",action="append",default=[],metavar="ID=PATH",help="Use this local Git checkout at its HEAD for update")
    args=parser.parse_args()
    configs=read(ROOT/"sources.json")
    local={k:Path(v).resolve() for k,v in (s.split("=",1) for s in args.checkout)}
    if local.keys()-{c["id"] for c in configs}:parser.error("Unknown checkout ID")
    with (ROOT/"Justfile").open() as lock:
        fcntl.flock(lock,fcntl.LOCK_EX if args.action in {"update","build"} else fcntl.LOCK_SH)
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
