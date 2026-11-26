"""Convert released study items and selected textbook sections to stable, plain-text notes."""
import json
import re
import unicodedata
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
FIELDS = ["ID", "Exam", "Section", "Topic", "Prompt", "Choices", "Answer", "Reason", "Source", "License", "Figure"]
CC = "MD3 contributors · CC BY 4.0 · https://creativecommons.org/licenses/by/4.0/ · adapted for Anki"
OS = "OpenStax, Rice University · CC BY-NC-SA 4.0 · https://creativecommons.org/licenses/by-nc-sa/4.0/ · adapted for Anki"
MICRO_CASES = {
    "hepatitis-b-acute-marker", "hepatitis-b-recovery-serology", "hepatitis-b-vaccine-serology",
    "micro-congenital-rubella-syndrome-recognition", "micro-hav-clinical-recognition", "micro-hav-igm-confirm",
    "micro-hepc-chronic", "micro-measles-clinical-recognition", "micro-measles-koplik",
    "micro-meningococcal-septicemia-recognition", "micro-mumps-parotitis-orchitis-recognition",
    "micro-pertussis-paroxysmal-stage", "micro-polio-flaccid-paralysis", "micro-rota-severe-ge",
    "micro-tetanus-lockjaw-recognition", "micro-zoster-phn", "micro-zoster-reactivation",
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def note(key, exam, section, topic, front, choices, answer, reason, source, license):
    return dict(zip(FIELDS, [key, exam, section, topic, front.strip(), choices, answer.strip(),
                             reason.strip(), source, license, ""], strict=True))


def simple(element):
    """Return text only when every essential piece can survive plain-text export."""
    if element is None:
        return ""
    pieces = []
    def visit(node):
        tag = node.tag.rsplit("}", 1)[-1]
        if tag in {"math", "media", "image", "table", "figure", "equation"}:
            raise ValueError("needs visual source")
        if tag == "link" and not "".join(node.itertext()).strip():
            raise ValueError("needs cross-reference")
        value = node.text or ""
        if tag in {"sup", "sub"}:
            original = "0123456789+-"
            target = "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻" if tag == "sup" else "₀₁₂₃₄₅₆₇₈₉₊₋"
            value = value.translate(str.maketrans(original, target)) if all(c in original for c in value) else f"({value})"
        pieces.append(value)
        for child in node:
            visit(child)
            pieces.append(child.tail or "")
    try:
        visit(element)
    except ValueError:
        return ""
    return " ".join("".join(pieces).split())


def fold(text):
    return unicodedata.normalize("NFKC", text).lower().replace("’", "'").strip()


def openstax(root, cfg, commit):
    book = cfg["id"]
    collection = ET.parse(root / "collections" / (book + ".collection.xml"))
    license = collection.find(".//{*}license").get("url", "")
    if license.replace("http:", "https:").rstrip("/") != "https://creativecommons.org/licenses/by-nc-sa/4.0":
        raise ValueError(f"Review changed license for {book}: {license}")
    terms = {fold(t) for t in (ROOT / "terms.txt").read_text().splitlines() if t and not t.startswith("#")}
    credit = OS + " · " + cfg["authors"] + " and contributors · https://openstax.org/books/" + book + "/pages/preface"
    chapters = set()
    for chapter in collection.findall(".//{*}subcollection"):
        title = chapter.findtext("{*}title")
        if title not in cfg["chapters"]:
            continue
        chapters.add(title)
        for module in chapter.findall("./{*}content/{*}module"):
            mid = module.get("document")
            path = f"modules/{mid}/index.cnxml"
            doc = ET.parse(root / path)
            section = simple(doc.find("{*}title"))
            base = f"OpenStax, {book}, {title} / {section} · https://github.com/{cfg['repo']}/blob/{commit}/{path}"
            for item in doc.findall(".//{*}glossary/{*}definition"):
                term = simple(item.find("{*}term"))
                meaning = simple(item.find("{*}meaning"))
                if fold(term) not in terms or not meaning:
                    continue
                key = f"{book}:{mid}:{item.attrib['id']}"
                yield note(key, "MCAT", cfg["section"], title, f"In {section.lower()}, what does “{term}” mean?",
                           "", meaning, "", base + "#" + item.attrib["id"], credit)
            if book != "psychology-2e":
                continue
            for item in doc.findall(".//{*}exercise"):
                problem = item.find("{*}problem")
                if problem is None:
                    continue
                paras = problem.findall("{*}para")
                options = [simple(o) for o in problem.findall("{*}list/{*}item")]
                key = simple(item.find("{*}solution")).strip(".").upper()
                if len(paras) != 1 or not options or not all(options) or not re.fullmatch("[A-E]", key):
                    continue
                stem = simple(paras[0])
                if not stem or ord(key)-65 >= len(options) or re.search(r"according to the (?:text|book)|this chapter|first (?:woman|person)|which year|^who (?:proposed|developed|created|of the following)|credited with the first",stem,re.I):
                    continue
                yield note(f"{book}:{mid}:{item.attrib['id']}", "MCAT", cfg["section"], title, stem,
                           "\n".join(options), options[ord(key)-65], "", base+"#"+item.attrib["id"], credit)
    if chapters != set(cfg["chapters"]):
        raise ValueError(f"{book} curriculum changed; check chapter selections: {set(cfg['chapters']) - chapters}")


SECTION_NAMES = {
    "anaes": "Anesthesiology", "biochem": "Biochemistry", "biostats": "Biostatistics",
    "cardio": "Cardiovascular", "derm": "Dermatology", "em": "Emergency medicine",
    "endo": "Endocrine", "gi": "Gastrointestinal", "gynae": "Reproductive and obstetric",
    "haem": "Hematology", "icu": "Critical care", "id": "Infectious diseases",
    "immuno": "Immunology", "msk": "Musculoskeletal", "neuro": "Nervous system",
    "obs": "Reproductive and obstetric", "ophth": "Ophthalmology", "paeds": "Pediatrics",
    "pharm": "Pharmacology", "psych": "Psychiatry", "resp": "Respiratory",
}



def cohort(root, cfg, commit):
    base = root / "open-content"
    attribution = f" · https://github.com/{cfg['repo']}/blob/{commit}/"
    for folder, meta, exam in [("usmle/step1","publicUsmle","USMLE Step 1"), ("modules","publicModule","USMLE Step 2 CK")]:
        path = base / folder
        allowed = set(read(path / "release-v1.json")["questionIds"])
        registry = read(path / "sources.json")["sources"]
        if isinstance(registry, list):
            registry = {entry["id"]:entry for entry in registry}
        for f in sorted((path/"questions").glob("*/*.json")):
            item = read(f)
            details = item[meta]
            if item["id"] not in allowed or item.get("imageUrl") or details.get("media"):
                continue
            if details["itemText"]["licence"] != "CC-BY-4.0":
                raise ValueError(f"Changed item license: {item['id']}")
            topic = f.parent.name
            if topic == "microbiology" and f.name.split(".")[0] not in MICRO_CASES:
                continue
            ref = registry[details["evidence"]["sourceId"]]
            url = ref.get("canonicalUrl") or ref.get("url")
            if not url:
                raise ValueError(f"Missing evidence URL: {item['id']}")
            if folder == "modules":
                if details.get("review",{}).get("verdict") != "passed":
                    continue
                # International clinical material supplies diagnostic reasoning; original US
                # cases cover jurisdiction-dependent management and care transitions.
                if item["questionType"] not in {"diagnosis","mechanism","investigation"}:
                    continue
            options = item["options"]
            correct = [o for o in options if o["isCorrect"]]
            if len(correct) != 1:
                raise ValueError(f"Ambiguous answer: {item['id']}")
            why = correct[0].get("explanation","")
            source = f"{ref['title']} · {url}" + attribution + f.relative_to(root).as_posix()
            yield note(item["id"],exam,SECTION_NAMES.get(topic, topic.title()),item["questionType"],
                       item["stem"],"\n".join(o["text"] for o in options),correct[0]["text"],why,source,CC)
    path = base/"modules"
    allowed = set(read(path/"cards-release-v1.json")["cardIds"])
    for f in sorted((path/"cards").glob("*/*.json")):
        data = read(f)
        if data["licence"] != "CC-BY-4.0":
            raise ValueError(f"Changed card-bank license: {f}")
        for card in data["cards"]:
            ref = card.get("reference")
            if card["id"] not in allowed or not ref or not ref.get("url"):
                continue
            if data["discipline"] not in {"anatomy","psych"}:
                continue
            if re.search(r"(?i:\b(?:structure|band|bone|nerve|marked|muscle|tendon)) [A-Z]\b", card["front"]):
                continue
            yield note(card["id"],"USMLE Step 1",SECTION_NAMES.get(data["discipline"], data["discipline"].title()),"Recall",card["front"].replace("[___]","_____"),
                       "",card["back"],card["context"],f"{ref['title']} · {ref['url']}"+attribution+f.relative_to(root).as_posix(),CC)
