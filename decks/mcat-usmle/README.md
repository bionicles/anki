# MCAT and USMLE

Open **File → Import** in Anki and select `decks/mcat-usmle/release/MCAT-USMLE.apkg`. Select the exam you are currently preparing for under **MCAT and USMLE**. The package contains 1,861 cards across four exams. Each subdeck has its own subject or task grouping. Every card carries a source and license on its back. [Anki package](release/MCAT-USMLE.apkg) · [Editable TSV](release/MCAT-USMLE.tsv) · [Topic counts and card IDs](release/coverage.tsv)

**Try a Step 3 case.** Ascitic fluid from a febrile patient with cirrhosis contains 800 nucleated cells/mm³, of which 50% are neutrophils. What is the absolute neutrophil count?

<details><summary>Check your answer</summary>

**400/mm³.** Multiply 800 by 0.50. A separately scheduled card gives a patient with 500 neutrophils/mm³, a negative culture and no apparent secondary source. It asks how the cell count should affect initial management. The two reviews distinguish calculating the count from acting on the result. [AASLD clinical guidance](https://www.aasld.org/practice-guidelines/diagnosis-evaluation-and-management-ascites-spontaneous-bacterial-peritonitis)

</details>

## What you can practice

| Exam | Cards | Material |
| --- | ---: | --- |
| MCAT | 929 | All four sections. Original questions map to all 31 numbered science content categories. Ten original CARS passages each anchor three separately graded comprehension, inference or application questions. Four additional science passages cover interpreting experiments. The OpenStax selection adds terminology and keyed psychology questions. |
| USMLE Step 1 | 610 | Foundational science mechanisms, short clinical stems, anatomy, pathology, physiology, pharmacology, epidemiology, and selected microbiology. Cases include reading oxygen dissociation and pressure–volume curves. |
| USMLE Step 2 CK | 200 | Diagnostic vignettes and investigations across clinical rotations. Original management cases cover emergency care, pediatrics, obstetrics, prevention, communication and surgery. |
| USMLE Step 3 | 122 | 27 Foundations of Independent Practice cards, 32 Advanced Clinical Medicine cards and 63 independently graded decisions across 17 CCS-style case topics. Practice interpreting new findings, selecting the next action, reassessing and planning follow-up. |

The coverage table gives actual card IDs for each topic. Counts indicate where the material is concentrated. MCAT passages are shorter than full exam passages. The clinical cases sample the USMLE outlines, and the case cards grade one decision at a time. For timed exams and practice entering orders, advancing time and responding to simulator feedback, use the official materials. A test-prep specialist or clinician has not independently validated this combined release. [AAMC outline](https://students-residents.aamc.org/prepare-mcat-exam/whats-mcat-exam-pdf-outline) · [Step 1](https://www.usmle.org/exam-resources/step-1-materials) · [Step 2 CK](https://www.usmle.org/exam-resources/step-2-ck-materials) · [Step 3 and sample cases](https://www.usmle.org/exam-resources/step-3-materials)

## Update or rebuild

From the repository root, run the following commands.

```sh
cd decks/mcat-usmle
just check-updates
just update
```

`check-updates` reports the local and remote revision for each configured source without modifying the release. `update` checks all six Git branches, fetches changed inputs at the reported commit, reapplies the selection rules and merges them with `originals.tsv`. It validates the artifacts in a temporary Anki collection before replacing `release/`. An unchanged run checks artifact hashes and leaves the package alone. Run the command whenever you want to pick up source changes. The original guideline-based cards need editorial review when clinical guidance changes.

`just build` rebuilds from the committed source snapshots without fetching the upstream repositories. The first installation of the pinned Python dependencies requires network access. `just figures` regenerates the eleven original plots. `just test` imports the package, checks all fields, media, deck assignments, tags and coverage, then exercises an editable TSV update against the same collection.

Re-import the updated package into the same Anki profile with note updates enabled. Stable note identities let Anki update the content and retain the card schedule. Anki can keep a local edit when using its default “if newer” update policy. The TSV uses the same GUIDs and requires the package note type to be installed first. Review `release/retired.tsv` for withdrawn identities. Search by `CardID` in Browse to decide whether to suspend a previously imported note.

## How the merge works

- `sources.json` specifies the upstream repositories, branches, adapters and textbook chapters. `terms.txt` selects relevant glossary headwords. The extractor uses Cohort's published release lists, individual licenses, evidence references and image-independence filters. It draws diagnostic and investigation questions from the international clinical module bank. The original cards add US-focused management.
- `release/sources.lock.json` records upstream revisions and checksums of the normalized snapshots. `release/build.json` records build inputs and artifact hashes. Each source note has a stable ID and a link back to its source. The editable package fields include the question, options, answer, explanation, source, license and figure.
- Exact duplicate prompts with equivalent options within an exam share a published identity. Conflicting keys stop the build. `release/aliases.tsv` records source-to-published IDs. Similar clinical vignettes testing different decisions remain independently scheduled.
- The package draws on five OpenStax books, MD3 contributors' Cohort question bank and original material. AnKing's separately distributed MCAT and Step decks can be obtained from their publishers. Paid subscriptions and third-party media are outside this updater. [AnKing](https://www.theanking.com/) · [Cohort](https://github.com/todd866/cohort) · [Source licenses and attribution](LICENSES.md)
