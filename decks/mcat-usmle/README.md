# MCAT and USMLE

Open **File → Import** in Anki and select `decks/mcat-usmle/release/MCAT-USMLE.apkg`. Select the exam you are currently preparing for under **MCAT and USMLE**. The package contains 4,949 cards across four exams. This is a supplemental release. The coverage audit is open for all four exams. Each subdeck has its own subject or task grouping. Every card carries a source and license on its back. [Anki package](release/MCAT-USMLE.apkg) · [Editable TSV](release/MCAT-USMLE.tsv) · [Topic counts and card IDs](release/coverage.tsv) · [Official outline mappings and gaps](blueprint.tsv)

**Try a Step 3 case.** Ascitic fluid from a febrile patient with cirrhosis contains 800 nucleated cells/mm³, of which 50% are neutrophils. What is the absolute neutrophil count?

<details><summary>Check your answer</summary>

**400/mm³.** Multiply 800 by 0.50. A separately scheduled card gives a patient with 500 neutrophils/mm³, a negative culture and no apparent secondary source. It asks how the cell count should affect initial management. The two reviews distinguish calculating the count from acting on the result. [AASLD clinical guidance](https://www.aasld.org/practice-guidelines/diagnosis-evaluation-and-management-ascites-spontaneous-bacterial-peritonitis)

</details>

## What you can practice

| Exam | Cards | Material |
| --- | ---: | --- |
| MCAT | 1,412 | All four sections and all 31 numbered science content categories have cards. Twelve original CARS passages support 42 independently graded questions. Seven science passages test experimental interpretation. Spectral windows, Fischer projections and a TLC plate give practice reading chemical data. Selected OpenStax exercises add application practice alongside glossary recall. |
| USMLE Step 1 | 1,392 | Mechanisms, clinical stems, tissue identification and interpretation of physiological curves and ECGs. The coverage check below explains the remaining gaps. |
| USMLE Step 2 CK | 1,134 | Cases on diagnosis, investigation, prevention and treatment. Examples include differentiating inherited disorders, evaluating a new mass, interpreting a rhythm strip, recognizing refeeding syndrome, distinguishing head CT findings and evaluating medication-induced movement disorders. |
| USMLE Step 3 | 1,011 | 84 Foundations of Independent Practice cards, 764 Advanced Clinical Medicine cards and 163 decisions across 54 CCS-style case topics. Two research or advertising stimuli support ten questions about clinical evidence. |

The outline map includes 150 finer MCAT science topic groups, along with the numbered categories, reasoning skills and clinical mappings. All 1,460 entries have partial coverage. For example, questions on alkene configuration can show whether a learner can assign priorities on a drawing. They leave open how the learner handles an unfamiliar molecule. The map links each reviewed objective to card IDs, the relevant official specifications and a concrete gap for further review. For example, it lists separate Step 1, Step 2 CK and Step 3 evidence for AV conduction disorders. The topic inventory lists every shipped card. Subject coverage, unfamiliar passage practice and performance on timed questions are separate things to check. The CCS cards let you rehearse individual decisions. The official simulator also tests order entry, sequencing, passage of time and response to evolving findings. This package has not undergone independent clinician or test-prep review. [Outline map](blueprint.tsv) · [Card inventory](release/coverage.tsv) · [AAMC outline](https://students-residents.aamc.org/prepare-mcat-exam/whats-mcat-exam-pdf-outline) · [USMLE Step 3 practice materials](https://www.usmle.org/exam-resources/step-3-materials)

## How much of each Step can you practice?

The audit starts with 174 topic families indexed to the 18 areas of the 2026 USMLE content outline. Each Step gets its own row for each family, including families still awaiting evidence. A family can contain dozens of clinical objectives. The counts below show where the deck has documented practice. They are lower bounds while card review continues. They do not predict an exam score. [Full scorecard](release/step-coverage.tsv) · [Topic inventory and official page references](step-families.tsv)

| Families out of 174 | Step 1 | Step 2 CK | Step 3 |
| --- | ---: | ---: | ---: |
| At least one reviewed card linked to the family | 125 | 135 | 132 |
| At least one objective with an applied case | 70 | 111 | 110 |
| At least one objective revisited on a different case | 52 | 92 | 81 |
| At least one objective with a foundation, application and different case | 42 | 49 | 66 |

### How much practice does an individual condition get?

The named-topic scorecard contains 1,085 conditions or clinical tasks indexed in eight of the 18 outline areas. Each has a row for every Step, including zeroes. A named topic earns a full sequence when its card IDs include a prerequisite, a case using it and a changed case, all tied to the **same reviewed objective in the same Step and family**. A topic can have separate foundation and transfer cards and still lack a sequence if they test different decisions. Each row links the cards and names the qualifying objectives. This is a conservative measure because both editorial registers must cite the relevant evidence. [Named-topic scorecard](release/step-item-coverage.tsv) · [Objective definitions and changed evidence](step-depth.tsv)

| Named topics out of 1,085 | Step 1 | Step 2 CK | Step 3 |
| --- | ---: | ---: | ---: |
| At least one specifically linked card | 417 | 486 | 435 |
| At least one application and changed case for the same objective | 52 | 100 | 96 |
| At least one full sequence for the same objective | 40 | 44 | 50 |

### Cardiovascular coverage

All 15 cardiovascular families have a linked card on every Step. At the finer level, we indexed 127 conditions and tasks from the two cardiovascular outline pages. The rows below are mutually exclusive and sum to 127 in each column. Run `just coverage` to see these four counts for every indexed system. Systems still awaiting a detailed inventory have a separate label. [Official cardiovascular outline](https://www.usmle.org/sites/default/files/2022-01/USMLE_Content_Outline_0.pdf#page=18) · [Named topics and evidence](release/step-item-coverage.tsv)

| Deepest documented practice for each cardiovascular topic | Step 1 | Step 2 CK | Step 3 |
| --- | ---: | ---: | ---: |
| No question specifically linked yet | 72 | 62 | 75 |
| Linked question, no application and changed-case pair | 48 | 53 | 32 |
| Case pair, still missing its prerequisite | 2 | 6 | 5 |
| Prerequisite, application and changed case on one objective | 5 | 6 | 15 |

For example, two patients with exertional leg pain have different resting ankle pressures. When the ankle-brachial index is 1.10, the learner selects exercise testing. When it is 1.50, the ankle arteries may be noncompressible and the next study is a toe-brachial index with waveforms. Other cards ask how to calculate the index from four pressure measurements and how the onset of weakness changes the urgency of treating an ischemic limb. Search Anki Browse for `tag:outline::cv::vascular tag:visual::question`. [ACC/AHA peripheral artery disease guideline](https://doi.org/10.1161/CIR.0000000000001251)

Thirty-six questions use nineteen new code-generated figures and two clinical ultrasound images. They include LV pressure–volume loops, pacemaker strips, oximetry runs, external aortic diameter measurements and venous compression studies. All nine named congenital topics now have linked questions on each Step. Rheumatic valve disease and constrictive pericarditis still have no specific link on any Step. [Clinical image credits](imaging.tsv) · [Reviewed objectives](step-depth.tsv)

### Endocrine coverage

The inventory groups the two endocrine outline pages into 82 named conditions or tasks across nine families. Each Step now has a specifically linked question for each of the 82 topics. Each family has at least one objective with a prerequisite, an application and a changed case. The table shows how often that depth extends to an individual topic. Interpreting a new concentrating test in partial vasopressin deficiency versus primary polydipsia remains an open objective. [USMLE endocrine outline](https://www.usmle.org/sites/default/files/2022-01/USMLE_Content_Outline_0.pdf#page=32) · [Named-topic scorecard](release/step-item-coverage.tsv)

| Endocrine topics out of 82 | Step 1 | Step 2 CK | Step 3 |
| --- | ---: | ---: | ---: |
| At least one specifically linked question | 82 | 82 | 82 |
| An application and a changed case for the same objective | 13 | 24 | 24 |
| A foundation, application and changed case for the same objective | 12 | 13 | 16 |

Thirty-five questions use fifteen code-generated figures and five clinical images. Search Anki Browse for `tag:outline::endo::pancreas tag:visual::question`. In two Step 3 cases, a learner reads serial laboratory results during treatment for diabetic ketoacidosis. Glucose falls in both. One patient still has elevated ketones and acidemia, while the other meets biochemical resolution criteria. Each decision is scheduled separately. The thyroid questions include uptake patterns and a specimen from a cervical lymph node. [Endocrine objectives and evidence](step-depth.tsv) · [Clinical image credits](imaging.tsv) · [Adult hyperglycemic-crisis consensus](https://doi.org/10.2337/dci24-0032)

### Reproductive system and breast

All three Steps have reviewed cards in each of the 11 families on the two outline pages for the female and transgender reproductive system and breast. The inventory splits those families into 104 conditions or clinical tasks. For example, the deck tests whether to investigate recurrent postmenopausal bleeding after an initially reassuring ultrasound, when to evaluate infertility, and how to locate the cause of amenorrhea from FSH and estradiol. Uterus didelphys and vulvar dysplasia still lack specifically linked questions on each Step. [USMLE outline](https://www.usmle.org/sites/default/files/2022-01/USMLE_Content_Outline_0.pdf#page=29) · [Named topics and card IDs](step-items.tsv)

| Reproductive and breast topics out of 104 | Step 1 | Step 2 CK | Step 3 |
| --- | ---: | ---: | ---: |
| At least one specifically linked question | 44 | 57 | 43 |
| An application and a changed case for the same objective | 8 | 20 | 15 |
| A foundation, application and changed case for the same objective | 7 | 9 | 11 |

Nine original figures and three clinical images support 19 visual questions. In Anki Browse, use `tag:outline::repro::fertility tag:visual::question` to practice reading contrast passage on a hysterosalpingogram. A learner first identifies free spill, then reads a new study with one blocked side. A clinical radiograph asks what the observed spill establishes about fertility. The Step 3 CCS-style cards also rehearse decisions during acute uterine bleeding, after a low-grade cervical screening abnormality and during pregnancy with cervical precancer. Each decision has its own card. [Image credits](imaging.tsv) · [2026 ASRM fertility evaluation](https://www.asrm.org/practice-guidance/practice-committee-documents/fertility-evaluation-of-infertile-women-a-committee-opinion-2026) · [2026 ACOG postmenopausal bleeding update](https://doi.org/10.1097/AOG.0000000000006275)

### Communication, ethics and patient safety

Each Step has a reviewed card in all 19 social-science families. The shared outline contains 143 more specific tasks in our inventory. For example, recognizing that an order check reduced errors and deciding whether it delayed urgent treatment are separately graded decisions. A second clinic supplies different measurements so the learner must read the graph again. Ten original teaching figures support 21 visual questions. In Anki Browse, try `tag:outline::social::quality tag:visual::question` for quality-improvement charts or `tag:outline::social::interview` for interviewing. [Official social-science outline](https://www.usmle.org/sites/default/files/2022-01/USMLE_Content_Outline_0.pdf#page=40) · [Task inventory and card IDs](step-items.tsv)

| Social-science tasks out of 143 | Step 1 | Step 2 CK | Step 3 |
| --- | ---: | ---: | ---: |
| Specifically linked question | 74 | 89 | 94 |
| Application and changed case for the same objective | 12 | 21 | 9 |
| Foundation, application and changed case for the same objective | 7 | 7 | 3 |

For a concrete gap, a retained foreign body after a procedure still has no linked safety question on any Step. The 143 tasks come from a shared outline. USMLE gives Step 1 communication and interpersonal skills a 6–9% band. Step 2 CK assigns 10–15% to the broader social-sciences category covering legal and ethical issues, professionalism, systems-based practice and patient safety. Step 3 assigns 7–9% of multiple-choice questions to social sciences. Use each exam’s specifications when prioritizing tasks. [Step 1 specifications](https://www.usmle.org/exam-resources/step-1-materials/step-1-content-outline-and-specifications) · [Step 2 CK specifications](https://www.usmle.org/exam-resources/step-2-ck-materials/step-2-ck-content-outline-specifications) · [Step 3 specifications](https://www.usmle.org/exam-resources/step-3-materials/step-3-content-outline-and-specifications)

### Hematology and lymphatic disorders

All six hematology families have linked cards on every Step. Of the 90 named topics in the two blood outline pages, Step 1 has specific evidence for 47, Step 2 CK for 57, and Step 3 for 52. Just four, three and three of those topics, respectively, have a documented full sequence. For example, the Step 2 CK splenic trauma questions teach when a patient can go to CT, then change the patient’s response to resuscitation so urgent operative control takes priority. Splenic abscess remains an open topic across all three Steps. [USMLE blood outline](https://www.usmle.org/sites/default/files/2022-01/USMLE_Content_Outline_0.pdf#page=6) · [Named-topic scorecard](release/step-item-coverage.tsv)

Ten blood and bone marrow photographs and thirteen schematic figures support 33 visual questions. One pair of aPTT mixing studies corrects initially in both cases. Only one stays corrected after incubation. Another set of cases asks the learner to tell a discrete protein peak from a broad gamma elevation and to explain why an absent peak cannot exclude light-chain disease. In Anki Browse, try `tag:outline::blood::clot tag:visual::question` or `tag:outline::blood::tumor tag:visual::question`. [Photographs and credits](imaging.tsv) · [World Federation of Hemophilia laboratory manual](https://elearning.wfh.org/wp-content/uploads/2025/04/wfh-lab-manual-third-edition-2025.pdf)

### What the respiratory family counts hide

Each Step now has reviewed cards in all ten respiratory families. A closer audit indexes 136 named conditions, causes or clinical topics from the two respiratory outline pages. Step 1 has specific card evidence for **27/136**, Step 2 CK for **34/136**, and Step 3 for **28/136**. For example, the obstructive-disease family contains asthma, bronchiectasis, COPD, chronic bronchitis and emphysema. A card about NIV for COPD earns credit for that topic. A separate card must actually test chronic bronchitis before that row earns credit. [Condition-by-condition evidence](step-items.tsv) · [Official respiratory outline](https://www.usmle.org/sites/default/files/2022-01/USMLE_Content_Outline_0.pdf#page=20)

These are editorial counting units. The inventory combines synonyms and repeated examples, groups some related infections, and retains general items where the outline includes a broader clinical task. Each row counts once per Step regardless of how many cards cite it. An empty Step cell means no specific question has been linked yet. The finer inventory currently covers cardiovascular medicine, endocrinology, hematology, respiratory medicine, gastroenterology, the nervous system and special senses, the female and transgender reproductive system and breast, and social sciences including communication and patient safety. Blank denominators for other systems in the scorecard mean their named-item inventory is pending.

In Anki Browse, try `tag:outline::lung::failure tag:practice::transfer` for reviewed cases. On one Step 2 CK card you classify pulmonary hypertension from catheterization measurements. On another, mean pulmonary artery pressure stays at 30 mm Hg while wedge pressure rises from 10 to 22 mm Hg and cardiac output changes. Seventeen code-generated figures provide 27 visual questions across the three Steps, including sleep recordings simulated from airflow and effort, forced expiratory curves, flow–volume loops and responses to noninvasive ventilation. [Objectives and card IDs](step-depth.tsv)

### Gastrointestinal coverage by Step

All three Steps have evidence in each of the 11 GI families. Counting specific conditions and clinical topics gives a more useful picture of breadth. One GI family contains both appendicitis and ischemic colitis. The deck has two independent appendiceal CTs, including a periappendiceal abscess. Ischemic colitis still has no specifically reviewed question on any Step. [Named topics and supporting cards](step-items.tsv) · [USMLE gastrointestinal outline](https://www.usmle.org/sites/default/files/2022-01/USMLE_Content_Outline_0.pdf#page=22)

| GI practice | Step 1 | Step 2 CK | Step 3 |
| --- | ---: | ---: | ---: |
| Named topics with a reviewed question | 50/183 | 56/183 | 47/183 |
| Families with one objective practiced from prerequisite through changed case | 5/11 | 8/11 | 11/11 |

Eleven patient images and eleven simulated plots support 34 GI visual questions. In Anki Browse, try `tag:outline::gi::bowel tag:visual::question` for CT, endoscopy and gastric-emptying studies. For Step 3, a patient with a nonbleeding visible vessel in an ulcer bed needs endoscopic hemostasis. A separate patient with a clean-based ulcer needs a different decision. The scorecard links each case and the evidence that changes the answer. [Clinical images and credits](imaging.tsv) · [Reviewed objectives](step-depth.tsv)

### Nervous system and special senses

Each Step has questions in all 18 families, but a count of individual conditions gives a different picture. The finer inventory has 220 entries across the four outline pages. It groups some related causes, such as organisms associated with bacterial meningitis. A question on a general syndrome cannot establish practice on every cause in that group. Optic neuritis, for example, still lacks a linked card on all three Steps. [Official outline](https://www.usmle.org/sites/default/files/2022-01/USMLE_Content_Outline_0.pdf#page=10) · [Named topics and evidence](step-items.tsv)

| Nervous system and special senses practice | Step 1 | Step 2 CK | Step 3 |
| --- | ---: | ---: | ---: |
| Individual topics with a linked question | 38/220 | 46/220 | 37/220 |
| Families with a prerequisite, application and changed case for one objective | 3/18 | 3/18 | 4/18 |

Fourteen code-generated figures support 27 visual questions. In Anki Browse, try `tag:outline::neuro::eye tag:visual::question` for paired monocular field maps. Step 1 asks where fibers cross and then shows unfamiliar patterns to localize. On Step 2 CK a patient with a known pituitary lesion develops abrupt homonymous field loss. The field pattern shifts attention behind the chiasm. On Step 3 a pair of independent cases asks what to do when vital capacity is falling and cough is weak, then when capacity is stable and the patient can protect their airway. The EEGs, audiograms and fields are teaching models. Interpretation of unfamiliar clinical recordings and formal perimetry remains an open objective. [Objectives and evidence](step-depth.tsv)

**What earns depth credit?** A foundation card asks for a prerequisite rule, relationship or mechanism. An application card makes the learner use an observation, measurement or patient history. A transfer card revisits that same decision with a new specimen, changed measurement, competing diagnosis or different clinical constraint. Each transfer entry names what changed and links the original application. A family earns the last row above only when all three levels belong to one objective within one Step. Restatements, answer explanations and the same visual reused on another card earn no additional transfer credit. [Objectives, card IDs and changed evidence](step-depth.tsv)

For example, take a newborn with a heart rate of 55/min. One Step 3 card asks what must be established before starting compressions. A second gives 30 seconds of ventilation with chest movement and asks what to add. The third changes one decisive finding: the chest never moved. The learner must now correct ventilation. The three cards can be studied independently and the answer changes when the evidence changes. [AHA/AAP neonatal resuscitation guideline](https://cpr.heart.org/en/resuscitation-science/cpr-and-ecc-guidelines/neonatal-resuscitation/)

Ten patient recordings let you practice locating a murmur between S1 and S2 or after S2. In Anki Browse, search `tag:listening::question` for the listening cards. For a different skill, two Step 1 cards ask you to read different Doppler envelopes and estimate the peak pressure gradient. Step 2 CK uses paired cases to distinguish primary from secondary mitral regurgitation. Step 3 changes anatomy or hemodynamic stability and asks whether the patient needs an intervention. [Recording sources](heart-sounds.tsv) · [Reviewed decisions](step-depth.tsv)

**Where to look next.** Run `just coverage` in this directory for a per-Step, per-system breakdown. In the scorecard, filter `MappedCards = 0` to find a topic family needing a card search and review. Filter `ApplicationObjectives > 0` and `TransferObjectives = 0` to find topics with a first case and no documented second case. Use the official percentage band to prioritize the parent system for that Step. A band applies to its entire published group. Step 3 bands apply to multiple-choice questions. The task-specific and CCS mappings are in the outline audit. Step 2 CK also has a cross-cutting nutrition discipline. Its items count in system categories as well. [Published weight groups](step-weights.tsv) · [Task mappings](blueprint.tsv) · [Step 1 specifications](https://www.usmle.org/exam-resources/step-1-materials/step-1-content-outline-and-specifications) · [Step 2 CK specifications](https://www.usmle.org/exam-resources/step-2-ck-materials/step-2-ck-content-outline-specifications) · [Step 3 specifications](https://www.usmle.org/exam-resources/step-3-materials/step-3-content-outline-and-specifications)

**Reproducing the audit.** Start from a specific outcome in the outline and write down what a learner would have to do before searching the cards. Append outcomes still awaiting review to `step-depth.tsv` with empty evidence fields. Inspect the question front and graded answer before assigning a stable card ID. A disease named in the stem as background does not establish an objective. The build checks exam ownership, unique evidence within each objective and independence of application and transfer media, including plots and audio from the same recording. In Anki Browse, search `tag:outline::ob::labor tag:practice::transfer` for reviewed examples. An empty cell is an audit lead. It may reflect an unreviewed existing card or a genuine content gap.

**Testing the learner.** To check whether practice transfers, reserve a new case, hide the topic and answer, and grade the first decision before feedback after a delay. Track the number correct and the number attempted separately for each Step and task. For Step 3, practice order entry and time progression in the official CCS interface as well. This release measures the practice available in the deck. Learner performance on held-out cases has yet to be measured. [Official Step 3 practice materials](https://www.usmle.org/exam-resources/step-3-materials)

### Step 1 coverage check

The original 610 cards included 570 Cohort items and 40 original questions. The current 1,392 include 822 originals. To practice tissue interpretation, 18 cards show nine unlabeled crops from microscope images. For example, one airway card asks you to identify the epithelial lining. A separately scheduled card asks how its apical surface helps clear particles. A further set of CDC images shows seven gross specimens and two liver micrographs, including an opened aorta, bilateral cystic kidneys and a stomach tumor. Other cards ask you to interpret ECG recordings and physiological or pharmacological plots. The endocrine and cardiovascular questions now connect drug targets to laboratory patterns and adverse effects. Each prescribing-information question cites the label for the product it describes. The new imaging questions include a normal head CT and examples of bleeding in four compartments. One card asks which vessels a subdural hematoma commonly injures. Another asks the learner to identify the collection on CT. In behavioral health, the new scenarios distinguish acute dystonia, akathisia and tardive dyskinesia by their time course and the patient’s movements. Important open gaps include recognition on unfamiliar specimens, imaging at other axial levels, and differentiation of secondary causes of psychiatric symptoms. [Card inventory](release/coverage.tsv) · [Official Step 1 specifications](https://www.usmle.org/exam-resources/step-1-materials/step-1-content-outline-and-specifications)

The Step 1 Communication section contains 50 cards, with another 32 in Communication and safety. The 70 Anatomy cards from Cohort are still classified as recall. USMLE assigns 6–9% of Step 1 to communication and interpersonal skills and explicitly includes interpretation of graphic material and specimens. A learner can encounter the name of a disease, recall its mechanism and still struggle to recognize a new clinical presentation. The audit records which of those tasks each reviewed card actually exercises. [Outline map](blueprint.tsv) · [USMLE system, competency and discipline weights](https://www.usmle.org/exam-resources/step-1-materials/step-1-content-outline-and-specifications)

## Update or rebuild

From the repository root, run the following commands.

```sh
cd decks/mcat-usmle
just check-updates
just update
```

`check-updates` reports the local and remote revision for each configured source without modifying the release. `update` checks all six Git branches, fetches changed inputs at the reported commit, reapplies the selection rules and merges them with `originals.tsv`. It validates the artifacts in a temporary Anki collection before replacing `release/`. An unchanged run checks artifact hashes and leaves the package alone. Run the command whenever you want to pick up source changes. The original guideline-based cards need editorial review when clinical guidance changes.

`just build` rebuilds from the committed source snapshots without fetching the upstream repositories. The first installation of the pinned Python dependencies requires network access. `just figures` regenerates the nineteen general-science figures, eight cardiovascular and renal plots plus nineteen cardiovascular studies, seventeen respiratory figures, eleven gastrointestinal figures, fourteen neurologic and special-senses figures, thirteen hematology figures, ten communication and quality-improvement figures, nine reproductive and breast figures, fifteen endocrine figures and fifteen simulated intrapartum monitors, labor curves and pressure figures. The nine OpenStax histology crops, nine CDC pathology photographs, eight ECG strips, seven recorded intrapartum windows and 51 diagnostic images are included in the package. Instructions for reproducing them are in the media credits. [Media credits](LICENSES.md) `just test` imports the package, checks all fields, media, deck assignments, tags and coverage, then exercises an editable TSV update against the same collection.

Re-import the updated package into the same Anki profile with note updates enabled. Stable note identities let Anki update the content and retain the card schedule. Anki can keep a local edit when using its default “if newer” update policy. The TSV uses the same GUIDs and requires the package note type to be installed first. Review `release/retired.tsv` for withdrawn identities. Search by `CardID` in Browse to decide whether to suspend a previously imported note.

## How the merge works

- `sources.json` specifies the upstream repositories, branches, adapters and textbook chapters. `terms.txt` selects relevant glossary headwords. The extractor uses Cohort's published release lists, individual licenses, evidence references and image-independence filters. It draws diagnostic and investigation questions from the international clinical module bank. The original cards add US-focused management.
- `release/sources.lock.json` records upstream revisions and checksums of the normalized snapshots. `release/build.json` records build inputs and artifact hashes. Each source note has a stable ID and a link back to its source. The editable package fields include the question, options, answer, explanation, source, license and figure.
- Exact duplicate prompts with equivalent options within an exam share a published identity. Conflicting keys stop the build. `release/aliases.tsv` records source-to-published IDs. Similar clinical vignettes testing different decisions remain independently scheduled.
- The package draws on five OpenStax books, MD3 contributors' Cohort question bank, ECGs from PhysioNet, CDC pathology photographs, individually credited diagnostic images and original material. AnKing's separately distributed MCAT and Step decks can be obtained from their publishers. Paid subscriptions and third-party media are outside this updater. [AnKing](https://www.theanking.com/) · [Cohort](https://github.com/todd866/cohort) · [Source licenses and attribution](LICENSES.md)
