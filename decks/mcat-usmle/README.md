# MCAT and USMLE

Open **File → Import** in Anki and select `decks/mcat-usmle/release/MCAT-USMLE.apkg`. Select the exam you are currently preparing for under **MCAT and USMLE**. The package contains 3,126 cards across four exams. This is a supplemental release. The coverage audit is open for all four exams. Each subdeck has its own subject or task grouping. Every card carries a source and license on its back. [Anki package](release/MCAT-USMLE.apkg) · [Editable TSV](release/MCAT-USMLE.tsv) · [Topic counts and card IDs](release/coverage.tsv) · [Official outline mappings and gaps](blueprint.tsv)

**Try a Step 3 case.** Ascitic fluid from a febrile patient with cirrhosis contains 800 nucleated cells/mm³, of which 50% are neutrophils. What is the absolute neutrophil count?

<details><summary>Check your answer</summary>

**400/mm³.** Multiply 800 by 0.50. A separately scheduled card gives a patient with 500 neutrophils/mm³, a negative culture and no apparent secondary source. It asks how the cell count should affect initial management. The two reviews distinguish calculating the count from acting on the result. [AASLD clinical guidance](https://www.aasld.org/practice-guidelines/diagnosis-evaluation-and-management-ascites-spontaneous-bacterial-peritonitis)

</details>

## What you can practice

| Exam | Cards | Material |
| --- | ---: | --- |
| MCAT | 1,412 | All four sections and all 31 numbered science content categories have cards. Twelve original CARS passages support 42 independently graded questions. Seven science passages test experimental interpretation. Spectral windows, Fischer projections and a TLC plate give practice reading chemical data. Selected OpenStax exercises add application practice alongside glossary recall. |
| USMLE Step 1 | 863 | Mechanisms, clinical stems, tissue identification and interpretation of physiological curves and ECGs. The coverage check below explains the remaining gaps. |
| USMLE Step 2 CK | 485 | Cases on diagnosis, investigation, prevention and treatment. Examples include differentiating inherited disorders, evaluating a new mass, interpreting a rhythm strip, recognizing refeeding syndrome, distinguishing head CT findings and evaluating medication-induced movement disorders. |
| USMLE Step 3 | 366 | 53 Foundations of Independent Practice cards, 206 Advanced Clinical Medicine cards and 107 decisions across 32 CCS-style case topics. Two research or advertising stimuli support ten questions about clinical evidence. |

The outline map includes 150 finer MCAT science topic groups, along with the numbered categories, reasoning skills and clinical mappings. All 498 entries have partial coverage. For example, questions on alkene configuration can show whether a learner can assign priorities on a drawing. They leave open how the learner handles an unfamiliar molecule. The map links each reviewed objective to card IDs, the relevant official specifications and a concrete gap for further review. For example, it lists separate Step 1, Step 2 CK and Step 3 evidence for AV conduction disorders. The topic inventory lists every shipped card. Subject coverage, unfamiliar passage practice and performance on timed questions are separate things to check. The CCS cards let you rehearse individual decisions. The official simulator also tests order entry, sequencing, passage of time and response to evolving findings. This package has not undergone independent clinician or test-prep review. [Outline map](blueprint.tsv) · [Card inventory](release/coverage.tsv) · [AAMC outline](https://students-residents.aamc.org/prepare-mcat-exam/whats-mcat-exam-pdf-outline) · [USMLE Step 3 practice materials](https://www.usmle.org/exam-resources/step-3-materials)

## How much of each Step can you practice?

The audit starts with 174 topic families indexed to the 18 areas of the 2026 USMLE content outline. Each Step gets its own row for each family, including families still awaiting evidence. A family can contain dozens of clinical objectives. The counts below show where the deck has documented practice. They are lower bounds while card review continues. They do not predict an exam score. [Full scorecard](release/step-coverage.tsv) · [Topic inventory and official page references](step-families.tsv)

| Families out of 174 | Step 1 | Step 2 CK | Step 3 |
| --- | ---: | ---: | ---: |
| At least one reviewed card linked to the family | 46 | 56 | 50 |
| At least one objective with an applied case | 12 | 23 | 20 |
| At least one objective revisited on a different case | 7 | 13 | 11 |
| At least one objective with a foundation, application and different case | 2 | 3 | 3 |

**What earns depth credit?** A foundation card asks for a prerequisite rule, relationship or mechanism. An application card makes the learner use an observation, measurement or patient history. A transfer card revisits that same decision with a new specimen, changed measurement, competing diagnosis or different clinical constraint. Each transfer entry names what changed and links the original application. A family earns the last row above only when all three levels belong to one objective within one Step. Restatements, answer explanations and the same visual reused on another card earn no additional transfer credit. [Objectives, card IDs and changed evidence](step-depth.tsv)

For example, take a newborn with a heart rate of 55/min. One Step 3 card asks what must be established before starting compressions. A second gives 30 seconds of ventilation with chest movement and asks what to add. The third changes one decisive finding: the chest never moved. The learner must now correct ventilation. The three cards can be studied independently and the answer changes when the evidence changes. [AHA/AAP neonatal resuscitation guideline](https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/neonatal-resuscitation/)

**Where to look next.** Run `just coverage` in this directory for a per-Step, per-system breakdown. In the scorecard, filter `MappedCards = 0` to find a topic family needing a card search and review. Filter `ApplicationObjectives > 0` and `TransferObjectives = 0` to find topics with a first case and no documented second case. Use the official percentage band to prioritize the parent system for that Step. A band applies to its entire published group. Step 3 bands apply to multiple-choice questions. The task-specific and CCS mappings are in the outline audit. Step 2 CK also has a cross-cutting nutrition discipline. Its items count in system categories as well. [Published weight groups](step-weights.tsv) · [Task mappings](blueprint.tsv) · [Step 1 specifications](https://www.usmle.org/exam-resources/step-1-materials/step-1-content-outline-and-specifications) · [Step 2 CK specifications](https://www.usmle.org/exam-resources/step-2-ck-materials/step-2-ck-content-outline-specifications) · [Step 3 specifications](https://www.usmle.org/exam-resources/step-3-materials/step-3-content-outline-and-specifications)

**Reproducing the audit.** Start from a specific outcome in the outline and write down what a learner would have to do before searching the cards. Append outcomes still awaiting review to `step-depth.tsv` with empty evidence fields. Inspect the question front and graded answer before assigning a stable card ID. A disease named in the stem as background does not establish an objective. The build checks exam ownership, unique evidence within each objective and independence of application and transfer images. In Anki Browse, search `tag:outline::ob::labor tag:practice::transfer` for reviewed examples. An empty cell is an audit lead. It may reflect an unreviewed existing card or a genuine content gap.

**Testing the learner.** To check whether practice transfers, reserve a new case, hide the topic and answer, and grade the first decision before feedback after a delay. Track the number correct and the number attempted separately for each Step and task. For Step 3, practice order entry and time progression in the official CCS interface as well. This release measures the practice available in the deck. Learner performance on held-out cases has yet to be measured. [Official Step 3 practice materials](https://www.usmle.org/exam-resources/step-3-materials)

### Step 1 coverage check

The original 610 cards included 570 Cohort items and 40 original questions. The current 863 include 293 originals. To practice tissue interpretation, 18 cards show nine unlabeled crops from microscope images. For example, one airway card asks you to identify the epithelial lining. A separately scheduled card asks how its apical surface helps clear particles. A further set of CDC images shows seven gross specimens and two liver micrographs, including an opened aorta, bilateral cystic kidneys and a stomach tumor. Other cards ask you to interpret ECG recordings and physiological or pharmacological plots. The endocrine and cardiovascular questions now connect drug targets to laboratory patterns and adverse effects. Each prescribing-information question cites the label for the product it describes. The new imaging questions include a normal head CT and examples of bleeding in four compartments. One card asks which vessels a subdural hematoma commonly injures. Another asks the learner to identify the collection on CT. In behavioral health, the new scenarios distinguish acute dystonia, akathisia and tardive dyskinesia by their time course and the patient’s movements. Important open gaps include recognition on unfamiliar specimens, imaging at other axial levels, and differentiation of secondary causes of psychiatric symptoms. [Card inventory](release/coverage.tsv) · [Official Step 1 specifications](https://www.usmle.org/exam-resources/step-1-materials/step-1-content-outline-and-specifications)

The Communication section grew from three to 16 cards. The 70 Anatomy cards from Cohort are still classified as recall. USMLE assigns 6–9% of Step 1 to communication and interpersonal skills and explicitly includes interpretation of graphic material and specimens. A learner can encounter the name of a disease, recall its mechanism and still struggle to recognize a new clinical presentation. The audit records which of those tasks each reviewed card actually exercises. [Outline map](blueprint.tsv) · [USMLE system, competency and discipline weights](https://www.usmle.org/exam-resources/step-1-materials/step-1-content-outline-and-specifications)

## Update or rebuild

From the repository root, run the following commands.

```sh
cd decks/mcat-usmle
just check-updates
just update
```

`check-updates` reports the local and remote revision for each configured source without modifying the release. `update` checks all six Git branches, fetches changed inputs at the reported commit, reapplies the selection rules and merges them with `originals.tsv`. It validates the artifacts in a temporary Anki collection before replacing `release/`. An unchanged run checks artifact hashes and leaves the package alone. Run the command whenever you want to pick up source changes. The original guideline-based cards need editorial review when clinical guidance changes.

`just build` rebuilds from the committed source snapshots without fetching the upstream repositories. The first installation of the pinned Python dependencies requires network access. `just figures` regenerates the nineteen general-science figures and fifteen simulated intrapartum monitors, labor curves and pressure figures. The nine OpenStax histology crops, nine CDC pathology photographs, eight ECG strips, seven recorded intrapartum windows and 20 diagnostic images are included in the package. Instructions for reproducing them are in the media credits. [Media credits](LICENSES.md) `just test` imports the package, checks all fields, media, deck assignments, tags and coverage, then exercises an editable TSV update against the same collection.

Re-import the updated package into the same Anki profile with note updates enabled. Stable note identities let Anki update the content and retain the card schedule. Anki can keep a local edit when using its default “if newer” update policy. The TSV uses the same GUIDs and requires the package note type to be installed first. Review `release/retired.tsv` for withdrawn identities. Search by `CardID` in Browse to decide whether to suspend a previously imported note.

## How the merge works

- `sources.json` specifies the upstream repositories, branches, adapters and textbook chapters. `terms.txt` selects relevant glossary headwords. The extractor uses Cohort's published release lists, individual licenses, evidence references and image-independence filters. It draws diagnostic and investigation questions from the international clinical module bank. The original cards add US-focused management.
- `release/sources.lock.json` records upstream revisions and checksums of the normalized snapshots. `release/build.json` records build inputs and artifact hashes. Each source note has a stable ID and a link back to its source. The editable package fields include the question, options, answer, explanation, source, license and figure.
- Exact duplicate prompts with equivalent options within an exam share a published identity. Conflicting keys stop the build. `release/aliases.tsv` records source-to-published IDs. Similar clinical vignettes testing different decisions remain independently scheduled.
- The package draws on five OpenStax books, MD3 contributors' Cohort question bank, ECGs from PhysioNet, CDC pathology photographs, individually credited diagnostic images and original material. AnKing's separately distributed MCAT and Step decks can be obtained from their publishers. Paid subscriptions and third-party media are outside this updater. [AnKing](https://www.theanking.com/) · [Cohort](https://github.com/todd866/cohort) · [Source licenses and attribution](LICENSES.md)
