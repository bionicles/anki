"""Measure documented USMLE practice against a fixed inventory of topic families."""
from collections import defaultdict

STEPS = ("USMLE Step 1", "USMLE Step 2 CK", "USMLE Step 3")
LEVELS = ("Foundation", "Application", "Transfer")


def measure(families, blueprint, depth, weights, cards):
    by_id = {card["ID"]: card for card in cards}
    by_family = {row["Family"]: row for row in families}
    if len(families) != len(by_family):
        raise ValueError("Duplicate Step family")
    topics = defaultdict(list)
    for row in blueprint:
        if row["Exam"] in STEPS and row["Axis"] == "Subtopic":
            topics[row["Domain"]].append(row)

    evidence = defaultdict(set)
    objectives = defaultdict(list)
    tags = defaultdict(set)
    seen_topics = set()
    for family, row in by_family.items():
        for topic in filter(None, row["BlueprintSubtopics"].split(" | ")):
            if topic not in topics or topic in seen_topics:
                raise ValueError(f"Unknown or duplicated subtopic: {topic}")
            seen_topics.add(topic)
            for item in topics[topic]:
                evidence[item["Exam"], family].update(item["ReviewedCardIDs"].split())

    seen_objectives = set()
    for row in depth:
        exam, family, objective = row["Exam"], row["Family"], row["Objective"]
        key = (exam, family, objective)
        if exam not in STEPS or family not in by_family or not objective or key in seen_objectives:
            raise ValueError(f"Invalid depth review: {key}")
        seen_objectives.add(key)
        ids = [row[level+"IDs"].split() for level in LEVELS]
        combined = [card_id for layer in ids for card_id in layer]
        state = row["ReviewState"]
        if state not in {"Awaiting review", "Documented"} or bool(combined) != (state == "Documented"):
            raise ValueError(f"Review status conflicts with evidence: {key}")
        if len(combined) != len(set(combined)):
            raise ValueError(f"Missing evidence or card reused within objective: {key}")
        if bool(ids[2]) != bool(row["ChangedEvidence"].strip()) or (ids[2] and not ids[1]):
            raise ValueError(f"Transfer needs an application and a changed case: {key}")
        for level, layer in zip(LEVELS, ids):
            for card_id in layer:
                if card_id not in by_id or by_id[card_id]["Exam"] != exam:
                    raise ValueError(f"Wrong Step or unpublished card: {key} {card_id}")
                tags[card_id].add("practice::" + level.lower())
        application_media = {by_id[k]["Figure"].rsplit(".", 1)[0] for k in ids[1]} - {""}
        if any(by_id[k]["Figure"].rsplit(".", 1)[0] in application_media for k in ids[2]):
            raise ValueError(f"Transfer reuses the original application media: {key}")
        objectives[exam, family].append(row)
        evidence[exam, family].update(combined)

    weight_groups = {}
    for group in weights:
        for system in group["Systems"].split():
            key = group["Exam"], system
            if key in weight_groups:
                raise ValueError(f"Duplicate exam weight group: {key}")
            weight_groups[key] = group
    required_groups = {(exam, k.split(".")[0]) for exam in STEPS for k in by_family}
    if set(weight_groups) != required_groups:
        raise ValueError("Exam weight references do not match the inventory")

    report = []
    for exam in STEPS:
        for family, row in by_family.items():
            linked = sorted(evidence[exam, family])
            for card_id in linked:
                if card_id not in by_id or by_id[card_id]["Exam"] != exam:
                    raise ValueError(f"Invalid family mapping: {exam} {family} {card_id}")
                tags[card_id].add("outline::" + family.replace(".", "::"))
            targets = objectives[exam, family]
            reviewed = [r for r in targets if r["ReviewState"] == "Documented"]
            weight = weight_groups[exam, family.split(".")[0]]
            result = dict(Exam=exam, Family=family, System=row["System"], Topic=row["Topic"],
                          Outline=row["Outline"], PublishedGroup=weight["PublishedGroup"],
                          GroupExamPercent=weight["ExamPercent"], WeightSource=weight["Source"], MappedCards=str(len(linked)),
                          TargetObjectives=str(len(targets)), ReviewedObjectives=str(len(reviewed)),
                          AwaitingDepthReview=str(len(targets)-len(reviewed)))
            for level in LEVELS:
                result[level+"Objectives"] = str(sum(bool(r[level+"IDs"]) for r in reviewed))
            result["ThreeLevelObjectives"] = str(sum(all(r[level+"IDs"] for level in LEVELS)
                                                     for r in reviewed))
            result["CardIDs"] = " ".join(linked)
            report.append(result)
    return report, tags


def display(report):
    print("Families with documented practice / families in scope")
    print("Exam or system                                 Mapped    Applied    Transfer   All three")
    def line(title, rows):
        counts = [sum(int(r[k]) > 0 for r in rows) for k in
                  ("MappedCards", "ApplicationObjectives", "TransferObjectives", "ThreeLevelObjectives")]
        print(f"{title:45}" + "".join(f"{n:4}/{len(rows):<4}  " for n in counts).rstrip())
    for exam in STEPS:
        rows = [r for r in report if r["Exam"] == exam]
        line(exam, rows)
        for system in dict.fromkeys(r["System"] for r in rows):
            line("  " + system, [r for r in rows if r["System"] == system])
