"""A named condition earns depth only within one Step, family and objective."""
import unittest

from step_coverage import STEPS, measure_item_depth


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
