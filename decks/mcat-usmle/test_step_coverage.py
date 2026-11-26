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

    def test_distinct_objectives_need_six_usable_cards(self):
        family = {"Family": "blood.cells", "System": "Hematology"}
        item = {"Family": "blood.cells", "Item": "Example", "Step1IDs": "f a t f2 a2 t2",
                "Step2CKIDs": "", "Step3IDs": ""}

        def objective(name, foundation, application, transfer):
            return dict(Exam=STEPS[0], Family="blood.cells", ReviewState="Documented",
                        Objective=name, FoundationIDs=foundation, ApplicationIDs=application,
                        TransferIDs=transfer)

        first = objective("First", "f f2", "a", "t")
        second = objective("Second", "f", "a2", "t2")
        result = measure_item_depth([family], [item], [first, second])
        self.assertEqual(result[0]["TwoObjectiveNames"], "First | Second")
        self.assertEqual(result[0]["TwoObjectiveCardIDs"], "f2 a t | f a2 t2")
        self.assertEqual(result[1]["TwoObjectiveCardIDs"], "")

        first = objective("First", "f", "a a2", "t")
        second = objective("Second", "f", "a2", "t2 f2")
        row = measure_item_depth([family], [item], [first, second])[0]
        self.assertEqual(row["ThreeLevelObjectives"], "2")
        self.assertEqual(row["TwoObjectiveCardIDs"], "")

    def test_bands_count_topics_once_despite_multiple_objectives(self):
        def topic(cards, paired, complete):
            return dict(MappedCards=str(cards), PairedObjectives=str(paired),
                        ThreeLevelObjectives=str(complete))

        rows = [topic(0, 0, 0), topic(2, 0, 0), topic(3, 1, 0), topic(7, 3, 2)]
        self.assertEqual(practice_bands(rows), (1, 1, 1, 1))


class MCATCARSCoverageTest(unittest.TestCase):
    def test_repeated_passage_and_unclassified_question(self):
        from deck import MCAT_CARS_SKILLS, mcat_cars_coverage

        blueprint = [dict(Exam="MCAT", Axis="Reasoning", Domain=skill, ReviewedCardIDs="")
                     for skill in MCAT_CARS_SKILLS]
        blueprint[0]["ReviewedCardIDs"] = "a science"
        blueprint[1]["ReviewedCardIDs"] = "b"
        def question(key, passage, section="Critical Analysis and Reasoning Skills"):
            return dict(ID=key, Exam="MCAT", Section=section, Topic="Shared topic",
                        Prompt=passage + "\n\nQuestion " + key)
        cards = [question("a", "One passage."), question("b", "One passage."),
                 question("c", "A different passage."), question("science", "One passage.", "Other")]
        first, second = mcat_cars_coverage(cards, blueprint)
        self.assertEqual((first["PassageWords"], first["Questions"], first["QuestionIDs"]), ("2", "2", "a b"))
        self.assertEqual((first["ComprehensionIDs"], first["WithinTextIDs"]), ("a", "b"))
        self.assertEqual((second["PassageWords"], second["UnclassifiedIDs"]), ("3", "c"))


class MCATScienceCoverageTest(unittest.TestCase):
    def test_outline_detail_requires_both_partners_in_the_same_category(self):
        from deck import MCAT_SCIENCE_SKILLS, mcat_detail_coverage

        def science(category, pairs):
            row = {column + "PairIDs": "" for column in MCAT_SCIENCE_SKILLS.values()}
            return dict(row, Subtopic=category + " · Energy", KnowledgePairIDs=pairs)

        def detail(name, ids):
            return dict(Exam="MCAT", Axis="Outline detail", Domain="1D · " + name,
                        ReviewedCardIDs=ids, Outline="source", NextAudit="Review a different case")

        reviewed = [science("1D", "a b | c d"), science("5E", "a c")]
        rows = mcat_detail_coverage([detail("Paired", "a b c"), detail("Split", "a c"),
                                     detail("Open", "")], reviewed)
        self.assertEqual([row["MappedCards"] for row in rows], ["3", "2", "0"])
        self.assertEqual([row["PairIDs"] for row in rows], ["a b", "", ""])

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


    def test_changed_case_requires_distinct_evidence_and_reviewed_skill(self):
        from deck import MCAT_SCIENCE_SKILLS, mcat_science_coverage

        rows = [dict(Exam="MCAT", Axis="Reasoning", Domain=skill, ReviewedCardIDs="a b")
                for skill in MCAT_SCIENCE_SKILLS]
        rows.append(dict(Exam="MCAT", Axis="Subtopic", Domain="topic", ReviewedCardIDs="a b",
                         Outline="source", NextAudit="review"))
        cards = [dict(ID=i, Exam="MCAT", Prompt=prompt, Figure="") for i, prompt
                 in [("a", "Study A\n\nFirst?"), ("b", "Study B\n\nSecond?")]]
        pair = dict(Subtopic="topic", Skill="Research design", Decision="Compare controls",
                    FirstID="a", TransferID="b", ChangedEvidence="Changed timing")
        def score(cards, pairs):
            return mcat_science_coverage(rows, cards, pairs)[0]
        self.assertEqual(score(cards, [pair])["ResearchDesignPairIDs"], "a b")
        for duplicate in ([pair, dict(pair, FirstID="b", TransferID="a")],
                          [dict(pair, TransferID="a")], [dict(pair, Skill="unknown")],
                          [dict(pair, ChangedEvidence=" ")], [dict(pair, FirstID="absent")]):
            with self.assertRaises(ValueError):
                score(cards, duplicate)
        for changed in (dict(Prompt=cards[0]["Prompt"]), dict(Prompt="Study A\n\nSecond?"),
                        dict(Figure="reused.png")):
            with self.assertRaises(ValueError):
                score([dict(cards[0], Figure="reused.png"), dict(cards[1], **changed)], [pair])
        rows[2]["ReviewedCardIDs"] = "a"
        with self.assertRaises(ValueError):
            score(cards, [pair])


class GapSummaryTest(unittest.TestCase):
    def test_unlinked_topics_do_not_also_count_in_linked_depth_gaps(self):
        from contextlib import redirect_stdout
        from io import StringIO
        from deck import display_gaps

        def topic(name, linked, full):
            return dict(Exam="USMLE Step 1", Family="cv.valve", Item=name,
                        MappedCards=str(linked), ThreeLevelObjectives=str(full))
        science = [dict(Subtopic="4E · Test topic", KnowledgeCards="0",
                        ProblemSolvingCards="2", ResearchDesignCards="0", DataInterpretationCards="1",
                        KnowledgePairs="0", ProblemSolvingPairs="0", ResearchDesignPairs="0", DataInterpretationPairs="1")]
        output = StringIO()
        with redirect_stdout(output):
            display_gaps([topic("Unlinked", 0, 0), topic("Linked", 2, 0), topic("Full", 4, 1)], science)
        lines = output.getvalue().splitlines()
        self.assertIn("4E (2)", lines[1])
        self.assertIn("Research design", lines[1])
        self.assertIn("Scientific knowledge", lines[1])
        self.assertIn("cv.valve (1) — Unlinked", lines[3])
        self.assertIn("cv.valve (1) — Linked", lines[5])
        self.assertNotIn("cv.valve (1) — Full", output.getvalue())
