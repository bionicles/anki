"""A named condition earns depth only within one Step, family and objective."""
import unittest

from step_coverage import STEPS, measure_item_depth, measure_system_depth, practice_bands


class NutritionCoverageTest(unittest.TestCase):
    def test_theme_overlap_and_empty_cells(self):
        from deck import NUTRITION_THEMES, nutrition_coverage
        cards = [dict(ID="c", Exam=STEPS[2], Section="CCS Cases", Figure="graph.webp")]
        blueprint = [dict(Exam=exam, Axis="Nutrition practice", Domain=theme,
                          ReviewedCardIDs="", NextAudit="Review another case")
                     for exam in STEPS for theme in NUTRITION_THEMES]
        blueprint[-1]["ReviewedCardIDs"] = blueprint[-2]["ReviewedCardIDs"] = "c"
        rows, tags = nutrition_coverage(cards, blueprint)
        self.assertEqual(len(rows), 18)
        self.assertEqual(rows[0]["Cards"], "0")
        self.assertEqual((rows[-1]["CCSIDs"], rows[-1]["VisualIDs"]), ("c", "c"))
        self.assertEqual(set(tags["c"]), {"nutrition::referral", "nutrition::treatment"})
        with self.assertRaises(ValueError):
            nutrition_coverage(cards, blueprint[1:])
        blueprint[0]["ReviewedCardIDs"] = "c"
        with self.assertRaises(ValueError):
            nutrition_coverage(cards, blueprint)


    def test_numbered_nutrition_skills_keep_step_and_empty_cells(self):
        from deck import nutrition_competency_coverage
        rows = [dict(Number=str(i), LearningTask="Task", TrainingLevel="UME", Priority="No",
                     Step1IDs="", Step2CKIDs="", Step3IDs="", Source="source") for i in range(1, 37)]
        rows[2]["Step2CKIDs"] = rows[5]["Step2CKIDs"] = "c"
        cards = [{"ID": "c", "Exam": STEPS[1]}]
        report, tags = nutrition_competency_coverage(cards, rows)
        self.assertEqual(len(report), 108)
        self.assertEqual({r["Exam"] for r in report if r["CardIDs"]}, {STEPS[1]})
        self.assertEqual(tags["c"], ["nutrition_skill::03", "nutrition_skill::06"])
        with self.assertRaises(ValueError):
            nutrition_competency_coverage(cards, rows[:-1])
        rows[0]["Step1IDs"] = "c"
        with self.assertRaises(ValueError):
            nutrition_competency_coverage(cards, rows)


class CCSTest(unittest.TestCase):
    def test_cross_topic_course_and_unreviewed_cards(self):
        from deck import ccs_coverage
        cards = [dict(ID=str(i), Exam=STEPS[2], Section="CCS Cases", Topic=topic, Prompt=str(i), Figure="")
                 for i, topic in enumerate(("Start", "Start", "Return", "Return"))]
        reviews = [dict(CardID=str(i), Domains=d) for i, d in enumerate(("Sequencing", "Therapy", "Location Timing"))]
        course = dict(Presentation="Fever", Decision="Where to treat", OpeningID="0", FirstOutcomeID="1",
                      ChangedOutcomeID="2", ChangedEvidence="Follow-up access changes.")
        report, tags = ccs_coverage(cards, reviews, [course])
        self.assertEqual(report[0]["UnreviewedIDs"], "3")
        self.assertEqual(report[0]["LocationIDs"], "2")
        self.assertEqual(report[1]["LocationIDs"], "")
        self.assertEqual(report[1]["PathwayCardIDs"], "0 1 2")
        self.assertIn("ccs_case::fever", tags["2"])
        with self.assertRaises(ValueError):
            ccs_coverage(cards, reviews, [dict(course, ChangedOutcomeID="0")])
        cards[1]["Figure"] = cards[2]["Figure"] = "shared.webp"
        with self.assertRaises(ValueError):
            ccs_coverage(cards, reviews, [course])
        with self.assertRaises(ValueError):
            ccs_coverage(cards, [dict(CardID="0", Domains="Background Therapy")], [])


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

    def test_exclusive_cases_must_share_an_objective_and_be_unique_across_families(self):
        families = [dict(Family="a", System="A"), dict(Family="b", System="B")]
        items = [dict(Family="a", Item="One", Step1IDs="a b c d e f", Step2CKIDs="", Step3IDs=""),
                 dict(Family="b", Item="One", Step1IDs="b c", Step2CKIDs="", Step3IDs="")]
        def objective(name, a, b):
            return dict(Exam=STEPS[0], Family="a", Objective=name, ReviewState="Documented",
                        FoundationIDs="", ApplicationIDs=a, TransferIDs=b)
        depth = [objective("First", "a", "b"), objective("Second", "c", "d")]
        row = measure_item_depth(families, items, depth)[0]
        self.assertEqual((row["PairedObjectives"], row["ExclusivePairIDs"]), ("2", ""))
        self.assertEqual((row["SharedApplicationIDs"], row["SharedTransferIDs"]), ("c", "b"))
        depth.append(objective("Third", "e", "f"))
        row = measure_item_depth(families, items, depth)[0]
        self.assertEqual((row["ExclusiveObjectiveNames"], row["ExclusivePairIDs"]), ("Third", "e f"))

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

    def test_system_counts_intersect_matching_topics_across_steps(self):
        rows = []
        # The two families use the same item label. Only A qualifies on Step 1,
        # and only B qualifies on Step 2, although both qualify on Step 3.
        for family, full in (("resp.a", (True, False, True)), ("resp.b", (False, True, True))):
            for exam, qualifies in zip(STEPS, full):
                rows.append(dict(System="Respiratory", Family=family, Item="Example", Exam=exam,
                                 MappedCards="3", ThreeLevelObjectives=str(int(qualifies)),
                                 TwoObjectiveCardIDs=""))
        for exam in STEPS:
            rows.append(dict(System="Respiratory", Family="resp.c", Item="Common", Exam=exam,
                             MappedCards="6", ThreeLevelObjectives="2",
                             TwoObjectiveCardIDs="f a t | g b u"))
        system, = measure_system_depth(rows)
        self.assertEqual(system["NamedTopics"], "3")
        self.assertEqual(system["AllStepsLinked"], "3")
        self.assertEqual([system[k+"FullSequence"] for k in ("Step1", "Step2CK", "Step3")],
                         ["2", "2", "3"])
        self.assertEqual(system["AllStepsFullSequence"], "1")
        self.assertEqual(system["AllStepsTwoObjectives"], "1")
        with self.assertRaises(ValueError):
            measure_system_depth(rows[:-1])
        with self.assertRaises(ValueError):
            measure_system_depth(rows + rows[:1])



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


    def test_component_membership_and_answer_length_ties(self):
        from deck import MCAT_CARS_SKILLS, mcat_cars_coverage

        blueprint = [dict(Exam="MCAT", Axis="Reasoning", Domain=skill,
                          ReviewedCardIDs="a b c d" if column == "Comprehension" else "")
                     for skill, column in MCAT_CARS_SKILLS.items()]
        component = dict(Exam="MCAT", Axis="CARS component",
                         Domain="Infer meaning from wording or structure", ReviewedCardIDs="a b c")
        cards = [dict(ID=key, Exam="MCAT", Section="Critical Analysis and Reasoning Skills",
                      Topic="Passage", Prompt="A passage.\n\nQuestion " + key,
                      Choices=options, Answer=answer)
                 for key, options, answer in [
                     ("a", "Short\nTwo words\nThree full words", "Three full words"),
                     ("b", "Also brief\nTwo words\nShort", "Two words"),
                     ("c", "One\nTwo words\nThree full words", "One"),
                     ("d", "", "Free response"),
                 ]]
        report, = mcat_cars_coverage(cards, blueprint + [component])
        self.assertEqual(report["RhetoricIDs"], "a b c")
        self.assertEqual(report["UnclassifiedComponentIDs"], "d")
        self.assertEqual(report["MultipleChoiceCards"], "3")
        self.assertEqual((report["LongestKeyIDs"], report["ShortestKeyIDs"]), ("a", "c"))
        for invalid in [dict(component, Domain="Evaluate an argument using passage evidence"),
                        dict(component, ReviewedCardIDs="missing"),
                        dict(component, Domain="Identify the thesis and explicit details")]:
            with self.assertRaises(ValueError):
                mcat_cars_coverage(cards, blueprint + [component, invalid])


class MCATScienceCoverageTest(unittest.TestCase):
    @staticmethod
    def case_cards():
        return [dict(Exam="MCAT", ID=key, Prompt="Question " + key, Figure="") for key in "abcd"]

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
                                     detail("Open", "")], reviewed, self.case_cards())
        self.assertEqual([row["MappedCards"] for row in rows], ["3", "2", "0"])
        self.assertEqual([row["PairIDs"] for row in rows], ["a b", "", ""])

    def test_second_pair_requires_four_distinct_cards_on_the_same_detail(self):
        from deck import MCAT_SCIENCE_SKILLS, mcat_detail_coverage

        topic = {col + "PairIDs": "" for col in MCAT_SCIENCE_SKILLS.values()}
        topic.update(Subtopic="3B · Transport", KnowledgePairIDs="a b | a c | b d")
        rows = [dict(Exam="MCAT", Axis="Outline detail", Domain="3B · " + detail,
                     ReviewedCardIDs=ids, Outline="source", NextAudit="review")
                for detail, ids in [("Overlapping", "a b c"), ("Independent", "a b c d")]]
        cards = self.case_cards()
        overlap, independent = mcat_detail_coverage(rows, [topic], cards)
        self.assertEqual(overlap["TwoIndependentPairIDs"], "")
        self.assertEqual(independent["TwoIndependentPairIDs"], "a c | b d")
        for changes in [({"Figure": "same.png"}, {"Figure": "same.png"}),
                        ({"Prompt": "Shared   data\n\nFirst?"}, {"Prompt": "shared data\n\nSecond?"})]:
            cards = self.case_cards()
            cards[0].update(changes[0])
            cards[1].update(changes[1])
            self.assertFalse(mcat_detail_coverage(rows, [topic], cards)[1]["TwoIndependentPairIDs"])


    def test_source_audit_keeps_missing_categories_and_unpaired_components_visible(self):
        from deck import mcat_source_audit

        science = [{"Subtopic": "7C · Learning"}, {"Subtopic": "9B · Demography"}]
        def component(name, links):
            return dict(Category="7C", Inventory="In progress", Outline="https://example.org/p",
                        Checkpoint=name, Details=links)
        detail = dict(Category="7C", Detail="Decision", ChangedPairs="1", TwoIndependentPairIDs="")
        uncovered, paired, pending = mcat_source_audit(science, [detail], [
            component("One", ""), component("Two", "Decision")])
        self.assertEqual(uncovered["AllDecisionsPaired"], "no")
        self.assertEqual((paired["AllDecisionsPaired"], paired["TwoPairDecisions"]), ("yes", "0"))
        self.assertEqual((pending["Inventory"], pending["AllDecisionsPaired"]), ("Awaiting source review", ""))
        with self.assertRaises(ValueError):
            mcat_source_audit(science, [detail], [component("Wrong", "Unlisted")])

    def test_detail_in_one_topic_does_not_cover_neighbors(self):
        from deck import MCAT_SCIENCE_SKILLS, mcat_topics_without_indexed_pairs

        def topic(name, pairs):
            row = {col + "PairIDs": "" for col in MCAT_SCIENCE_SKILLS.values()}
            return dict(row, Subtopic=name, ResearchDesignPairIDs=pairs)

        science = [topic("3B · Bone", "a b | c d"), topic("3B · Skin", "a d"),
                   topic("2A · Membranes", "a b"), topic("2A · Nucleus", "")]
        details = [dict(Category="3B", PairIDs="a b"), dict(Category="2A", PairIDs="")]
        self.assertEqual(mcat_topics_without_indexed_pairs(science, details),
                         ["3B · Skin", "2A · Membranes", "2A · Nucleus"])

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

    def test_second_objective_workload_requires_a_first_sequence_and_distinct_evidence(self):
        from contextlib import redirect_stdout
        from io import StringIO
        from deck import display_gaps

        rows = [
            dict(Exam="USMLE Step 1", Family="msk.trauma", Item=name, MappedCards="6",
                 ThreeLevelObjectives=str(count), TwoObjectiveCardIDs=evidence)
            for name, count, evidence in [
                ("No sequence", 0, ""), ("Shared cards", 2, ""),
                ("Independent", 2, "a b c | d e f"),
            ]
        ]
        output = StringIO()
        with redirect_stdout(output):
            display_gaps(rows, [])
        lines = output.getvalue().splitlines()
        self.assertIn("USMLE Step 1 • full-sequence topics with two independent objectives: 1/2", lines)
        index = lines.index("USMLE Step 1 • full-sequence topics awaiting a second objective, by family")
        self.assertEqual(lines[index + 1].strip(), "msk.trauma (1) — Shared cards")

    def test_unmapped_on_every_step_requires_three_explicit_zeroes(self):
        from contextlib import redirect_stdout
        from io import StringIO
        from deck import STEPS, display_gaps

        rows = []
        for exam in STEPS:
            for family, item, linked in [("neuro.spine", "Myelopathy", False),
                                         ("neuro.drug", "Myelopathy", exam == STEPS[-1])]:
                rows.append(dict(Exam=exam, Family=family, Item=item,
                                 MappedCards=str(int(linked)), ThreeLevelObjectives="0"))
        rows.append(dict(Exam=STEPS[0], Family="neuro.spine", Item="Partial inventory",
                         MappedCards="0", ThreeLevelObjectives="0"))
        output = StringIO()
        with redirect_stdout(output):
            display_gaps(rows, [])
        self.assertIn("Named topics missing a full sequence on at least one USMLE Step • 3", output.getvalue())
        self.assertIn("  Missing on 1 of 3 Steps • 1", output.getvalue())
        self.assertIn("  Missing on 3 of 3 Steps • 2", output.getvalue())
        self.assertIn("Named topics with no full sequence on any USMLE Step • 2", output.getvalue())
        self.assertEqual(output.getvalue().splitlines()[-2:], [
            "Named topics without a linked card on any USMLE Step • 1",
            "  neuro.spine (1) — Myelopathy",
        ])
