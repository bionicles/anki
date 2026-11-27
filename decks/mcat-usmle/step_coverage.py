"""Measure documented USMLE practice against a fixed inventory of topic families."""
from collections import defaultdict
from itertools import combinations, product

STEPS = ("USMLE Step 1", "USMLE Step 2 CK", "USMLE Step 3")
LEVELS = ("Foundation", "Application", "Transfer")


def measure(families, blueprint, depth, weights, cards, details=()):
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

    # A named condition within a family has its own evidence for each Step.
    # Preserve an empty denominator for systems without a fine-grained inventory.
    named_items = defaultdict(set)
    named_evidence = defaultdict(set)
    for row in details:
        family, item = row["Family"], row["Item"]
        if family not in by_family or not item.strip() or item in named_items[family]:
            raise ValueError(f"Unknown family or duplicate/empty outline item: {family} {item}")
        named_items[family].add(item)
        for exam, column in zip(STEPS, ("Step1IDs", "Step2CKIDs", "Step3IDs")):
            ids = row[column].split()
            if len(ids) != len(set(ids)) or any(k not in by_id or by_id[k]["Exam"] != exam for k in ids):
                raise ValueError(f"Invalid outline item evidence: {exam} {family} {item}")
            if ids:
                named_evidence[exam, family].add(item)
                evidence[exam, family].update(ids)
    detailed_systems = {by_family[f]["System"] for f in named_items}
    for family, row in by_family.items():
        if row["System"] in detailed_systems and family not in named_items:
            raise ValueError(f"Detailed system missing a family: {family}")

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
            result["NamedItemsInScope"] = str(len(named_items[family])) if family in named_items else ""
            result["NamedItemsMapped"] = str(len(named_evidence[exam, family])) if family in named_items else ""
            result["CardIDs"] = " ".join(linked)
            report.append(result)
    return report, tags


def distinct_objective_pair(complete):
    """Find two reviewed objectives with six distinct card IDs, in level order."""
    for (name, first), (other_name, second) in combinations(complete.items(), 2):
        for triple in product(*(sorted(layer) for layer in first)):
            # A validated objective already has disjoint IDs across its own levels.
            remaining = [layer.difference(triple) for layer in second]
            if all(remaining):
                other_triple = [min(layer) for layer in remaining]
                return (name + " | " + other_name,
                        " ".join(triple) + " | " + " ".join(other_triple))
    return "", ""


def measure_item_depth(families, items, objectives):
    """Only count an evidence card when both editorial registers cite it."""
    systems = {row["Family"]: row["System"] for row in families}
    grouped = defaultdict(list)
    for row in objectives:
        if row["ReviewState"] == "Documented":
            layers = [set(row[level+"IDs"].split()) for level in LEVELS]
            grouped[row["Exam"], row["Family"]].append((row["Objective"], layers))

    report = []
    for item in items:
        family = item["Family"]
        for exam, column in zip(STEPS, ("Step1IDs", "Step2CKIDs", "Step3IDs")):
            cited = set(item[column].split())
            row = dict(Exam=exam, System=systems[family], Family=family, Item=item["Item"],
                       MappedCards=str(len(cited)), CardIDs=" ".join(sorted(cited)))
            linked = [set() for level in LEVELS]
            paired, complete = [], {}
            for objective, layers in grouped[exam, family]:
                overlaps = [cited & layer for layer in layers]
                for matched, overlap in zip(linked, overlaps):
                    matched.update(overlap)
                if overlaps[1] and overlaps[2]:
                    paired.append(objective)
                    if overlaps[0]:
                        complete[objective] = overlaps
            for level, matched in zip(LEVELS, linked):
                row[level+"IDs"] = " ".join(sorted(matched))
            row["PairedObjectives"] = str(len(paired))
            row["ThreeLevelObjectives"] = str(len(complete))
            row["PairedObjectiveNames"] = " | ".join(paired)
            row["ThreeLevelObjectiveNames"] = " | ".join(complete)
            row["TwoObjectiveNames"], row["TwoObjectiveCardIDs"] = distinct_objective_pair(complete)
            report.append(row)
    return report



def measure_system_depth(item_report):
    """Count the same indexed topics across Steps, including intersections."""
    grouped = defaultdict(lambda: defaultdict(dict))
    for row in item_report:
        topic = (row["Family"], row["Item"])
        exam = row["Exam"]
        steps = grouped[row["System"]][topic]
        if exam not in STEPS or exam in steps:
            raise ValueError(f"Unexpected or duplicate Step for {topic}: {exam}")
        steps[exam] = (
            int(row["MappedCards"]) > 0,
            int(row["ThreeLevelObjectives"]) > 0,
            bool(row["TwoObjectiveCardIDs"]),
        )

    report = []
    for system, topics in sorted(grouped.items()):
        result = {"System": system, "NamedTopics": str(len(topics))}
        if any(set(steps) != set(STEPS) for steps in topics.values()):
            raise ValueError(f"Incomplete named-topic Step inventory for {system}")
        for index, measure_name in enumerate(("Linked", "FullSequence", "TwoObjectives")):
            for exam, prefix in zip(STEPS, ("Step1", "Step2CK", "Step3")):
                count = sum(steps[exam][index] for steps in topics.values())
                result[prefix + measure_name] = str(count)
            common = sum(all(steps[exam][index] for exam in STEPS) for steps in topics.values())
            result["AllSteps" + measure_name] = str(common)
        report.append(result)
    return report


def practice_bands(rows):
    """Place each named topic in its deepest documented practice band."""
    total = len(rows)
    linked = sum(int(r["MappedCards"]) > 0 for r in rows)
    paired = sum(int(r["PairedObjectives"]) > 0 for r in rows)
    complete = sum(int(r["ThreeLevelObjectives"]) > 0 for r in rows)
    return total - linked, linked - paired, paired - complete, complete


def display(report, item_report=()):
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

    if item_report:
        print("Named topics by deepest documented practice; each topic is counted once per Step")
        systems = list(dict.fromkeys(r["System"] for r in report))
        grouped = defaultdict(list)
        for item in item_report:
            grouped[item["Exam"], item["System"]].append(item)
        for exam in STEPS:
            print(exam)
            print(f"{'System':45}{'No link':>9}{'No pair¹':>10}{'Pair only':>11}{'Full':>7}{'Total':>8}")
            for system in systems:
                topics = grouped[exam, system]
                if topics:
                    bands = practice_bands(topics)
                    print(f"{system:45}{bands[0]:9}{bands[1]:10}{bands[2]:11}{bands[3]:7}{len(topics):8}")
                else:
                    print(f"{system:45}  Named topics not yet inventoried")
        print("¹ Linked to a card, with no documented application and changed case for the same objective.")
        print("Named topics meeting the same threshold on each of the three Steps")
        print(f"{'System':45}{'Linked':>8}{'Sequence':>10}{'Two objectives':>16}{'Total':>8}")
        for system in measure_system_depth(item_report):
            print(f"{system['System']:45}{system['AllStepsLinked']:>8}{system['AllStepsFullSequence']:>10}"
                  f"{system['AllStepsTwoObjectives']:>16}{system['NamedTopics']:>8}")
        print("Named items across inventoried systems (mapped / paired cases / three levels / two objectives with six distinct cards)")
        for exam in STEPS:
            rows = [r for r in item_report if r["Exam"] == exam]
            counts = [sum(int(r[key]) > 0 for r in rows) for key in
                      ("MappedCards", "PairedObjectives", "ThreeLevelObjectives")]
            counts.append(sum(bool(r["TwoObjectiveCardIDs"]) for r in rows))
            print(f"  {exam}: " + " / ".join(map(str, counts)) + f" of {len(rows)} named items")

    else:
        audited = [row for row in report if row["NamedItemsInScope"]]
        if audited:
            print("Named outline items with linked evidence (systems inventoried in detail)")
            for system in dict.fromkeys(row["System"] for row in audited):
                for exam in STEPS:
                    rows = [r for r in audited if r["Exam"] == exam and r["System"] == system]
                    numerator = sum(int(r["NamedItemsMapped"]) for r in rows)
                    denominator = sum(int(r["NamedItemsInScope"]) for r in rows)
                    print(f"  {system} · {exam}: {numerator}/{denominator}")
