"""A named condition earns depth only within one Step, family and objective."""
import unittest

from step_coverage import STEPS, measure_item_depth, practice_bands


class NamedDepthTest(unittest.TestCase):
    def test_matching_all_three_layers(self):
        family = {"Family": "blood.clot", "System": "Hematology"}
        item = {"Family": "blood.clot", "Item": "Example",
                "Step1IDs": "f a t", "Step2CKIDs": "", "Step3IDs": ""}

        def objective(name, foundation="", application="", transfer="", **changes):
            return dict({"Exam": STEPS[0], "Family": family["Family"], "Objective": name,
                         "ReviewState": "Documented", "FoundationIDs": foundation,
                         "ApplicationIDs": application, "TransferIDs": transfer}, **changes)

        unrelated = [
            objective("Prerequisite only", "f"),
            objective("Two cases only", "other", "a", "t"),
            objective("Another Step", "f", "a", "t", Exam=STEPS[1]),
            objective("Another family", "f", "a", "t", Family="blood.cells"),
        ]
        first, second, third = measure_item_depth([family], [item], unrelated)
        self.assertEqual((first["PairedObjectives"], first["ThreeLevelObjectives"]), ("1", "0"))
        for empty in (second, third):
            self.assertEqual((empty["MappedCards"], empty["PairedObjectives"],
                              empty["ThreeLevelObjectives"]), ("0", "0", "0"))

        complete = objective("One linked sequence", "f", "a", "t")
        first = measure_item_depth([family], [item], unrelated + [complete])[0]
        self.assertEqual(first["ThreeLevelObjectiveNames"], "One linked sequence")
        self.assertEqual(first["PairedObjectives"], "2")

    def test_bands_count_topics_once_despite_multiple_objectives(self):
        def topic(cards, paired, complete):
            return dict(MappedCards=str(cards), PairedObjectives=str(paired),
                        ThreeLevelObjectives=str(complete))

        rows = [topic(0, 0, 0), topic(2, 0, 0), topic(3, 1, 0), topic(7, 3, 2)]
        self.assertEqual(practice_bands(rows), (1, 1, 1, 1))


class MCATScienceCoverageTest(unittest.TestCase):
    def test_only_shared_evidence_counts_for_each_skill(self):
        from deck import MCAT_SCIENCE_SKILLS, mcat_science_coverage

        def row(axis, name, evidence, exam="MCAT"):
            return dict(Exam=exam, Axis=axis, Domain=name, ReviewedCardIDs=evidence,
                        Outline="source", NextAudit="review")

        rows = [row("Reasoning", skill, "") for skill in MCAT_SCIENCE_SKILLS]
        rows[0]["ReviewedCardIDs"] = "a b"
        rows[2]["ReviewedCardIDs"] = "b elsewhere"
        rows += [row("Subtopic", "first", "a b c"), row("Subtopic", "empty", ""),
                 row("Subtopic", "another exam", "a", exam="USMLE Step 1"),
                 row("Reasoning", "CARS comprehension", "c")]
        first, empty = mcat_science_coverage(rows)
        self.assertEqual(first["MappedCards"], "3")
        self.assertEqual(first["KnowledgeIDs"], "a b")
        self.assertEqual(first["ResearchDesignIDs"], "b")
        self.assertEqual(first["UnclassifiedIDs"], "c")
        self.assertEqual(empty["DataInterpretationCards"], "0")
