# MCAT and USMLE

Open **File → Import** in Anki and select `decks/mcat-usmle/release/MCAT-USMLE.apkg`. Select the exam you are currently preparing for under **MCAT and USMLE**. The package contains 2,478 cards across four exams. This is a supplemental release. The coverage audit is open for all four exams. Each subdeck has its own subject or task grouping. Every card carries a source and license on its back. [Anki package](release/MCAT-USMLE.apkg) · [Editable TSV](release/MCAT-USMLE.tsv) · [Topic counts and card IDs](release/coverage.tsv) · [Official outline mappings and gaps](blueprint.tsv)

**Try a Step 3 case.** Ascitic fluid from a febrile patient with cirrhosis contains 800 nucleated cells/mm³, of which 50% are neutrophils. What is the absolute neutrophil count?

<details><summary>Check your answer</summary>

**400/mm³.** Multiply 800 by 0.50. A separately scheduled card gives a patient with 500 neutrophils/mm³, a negative culture and no apparent secondary source. It asks how the cell count should affect initial management. The two reviews distinguish calculating the count from acting on the result. [AASLD clinical guidance](https://www.aasld.org/practice-guidelines/diagnosis-evaluation-and-management-ascites-spontaneous-bacterial-peritonitis)

</details>

## What you can practice

| Exam | Cards | Material |
| --- | ---: | --- |
| MCAT | 1,274 | All four sections and all 31 numbered science content categories have cards. Eleven original CARS passages support 36 independently graded questions. Seven science passages test experimental interpretation. Selected OpenStax exercises add application practice alongside glossary recall. |
| USMLE Step 1 | 719 | Mechanisms, clinical stems, tissue identification and interpretation of physiological curves and ECGs. The coverage check below explains the remaining gaps. |
| USMLE Step 2 CK | 288 | Cases on diagnosis, investigation, prevention and treatment. Examples include differentiating inherited disorders, evaluating a new mass and interpreting a rhythm strip. |
| USMLE Step 3 | 197 | 42 Foundations of Independent Practice cards, 78 Advanced Clinical Medicine cards and 77 decisions across 22 CCS-style case topics. Two research or advertising stimuli support ten questions about clinical evidence. |

The outline map links each reviewed objective to card IDs, the relevant official specifications and a concrete gap for further review. For example, it lists separate Step 1, Step 2 CK and Step 3 evidence for AV conduction disorders. The topic inventory lists every shipped card. Subject coverage, unfamiliar passage practice and performance on timed questions are separate things to check. The CCS cards let you rehearse individual decisions. The official simulator also tests order entry, sequencing, passage of time and response to evolving findings. This package has not undergone independent clinician or test-prep review. [Outline map](blueprint.tsv) · [Card inventory](release/coverage.tsv) · [AAMC outline](https://students-residents.aamc.org/prepare-mcat-exam/whats-mcat-exam-pdf-outline) · [USMLE Step 3 practice materials](https://www.usmle.org/exam-resources/step-3-materials)

### Step 1 coverage check

The original 610 cards included 570 Cohort items and 40 original questions. The current 719 include 149 originals. To practice tissue interpretation, 18 cards show nine unlabeled crops from microscope images. For example, one airway card asks you to identify the epithelial lining. A separately scheduled card asks how its apical surface helps clear particles. Other cards ask you to interpret ECG recordings and three physiological or pharmacological plots. Gross specimen interpretation, radiographic anatomy and recognition across independent pathology specimens still need broader coverage. [Card inventory](release/coverage.tsv) · [Official Step 1 specifications](https://www.usmle.org/exam-resources/step-1-materials/step-1-content-outline-and-specifications)

The Communication section grew from three to 16 cards. The 70 Anatomy cards from Cohort are still classified as recall. USMLE assigns 6–9% of Step 1 to communication and interpersonal skills and explicitly includes interpretation of graphic material and specimens. A learner can encounter the name of a disease, recall its mechanism and still struggle to recognize a new clinical presentation. The audit records which of those tasks each reviewed card actually exercises. [Outline map](blueprint.tsv) · [USMLE system, competency and discipline weights](https://www.usmle.org/exam-resources/step-1-materials/step-1-content-outline-and-specifications)

## Update or rebuild

From the repository root, run the following commands.

```sh
cd decks/mcat-usmle
just check-updates
just update
```

`check-updates` reports the local and remote revision for each configured source without modifying the release. `update` checks all six Git branches, fetches changed inputs at the reported commit, reapplies the selection rules and merges them with `originals.tsv`. It validates the artifacts in a temporary Anki collection before replacing `release/`. An unchanged run checks artifact hashes and leaves the package alone. Run the command whenever you want to pick up source changes. The original guideline-based cards need editorial review when clinical guidance changes.

`just build` rebuilds from the committed source snapshots without fetching the upstream repositories. The first installation of the pinned Python dependencies requires network access. `just figures` regenerates the eleven original model and data plots. The nine histology crops and eight ECG strips are included in the package. Instructions for reproducing them are in the media credits. [Media credits](LICENSES.md) `just test` imports the package, checks all fields, media, deck assignments, tags and coverage, then exercises an editable TSV update against the same collection.

Re-import the updated package into the same Anki profile with note updates enabled. Stable note identities let Anki update the content and retain the card schedule. Anki can keep a local edit when using its default “if newer” update policy. The TSV uses the same GUIDs and requires the package note type to be installed first. Review `release/retired.tsv` for withdrawn identities. Search by `CardID` in Browse to decide whether to suspend a previously imported note.

## How the merge works

- `sources.json` specifies the upstream repositories, branches, adapters and textbook chapters. `terms.txt` selects relevant glossary headwords. The extractor uses Cohort's published release lists, individual licenses, evidence references and image-independence filters. It draws diagnostic and investigation questions from the international clinical module bank. The original cards add US-focused management.
- `release/sources.lock.json` records upstream revisions and checksums of the normalized snapshots. `release/build.json` records build inputs and artifact hashes. Each source note has a stable ID and a link back to its source. The editable package fields include the question, options, answer, explanation, source, license and figure.
- Exact duplicate prompts with equivalent options within an exam share a published identity. Conflicting keys stop the build. `release/aliases.tsv` records source-to-published IDs. Similar clinical vignettes testing different decisions remain independently scheduled.
- The package draws on five OpenStax books, MD3 contributors' Cohort question bank, ECGs from PhysioNet and original material. AnKing's separately distributed MCAT and Step decks can be obtained from their publishers. Paid subscriptions and third-party media are outside this updater. [AnKing](https://www.theanking.com/) · [Cohort](https://github.com/todd866/cohort) · [Source licenses and attribution](LICENSES.md)
