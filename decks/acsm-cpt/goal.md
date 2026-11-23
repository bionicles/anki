Build an importable Anki deck for someone studying for the ACSM Certified Personal Trainer exam from scratch. Aim for **1,000 cards**, with **850–1,200** as a flexible range. The goal is to cover every published exam objective and practice the decisions a trainer has to make. Deliver the finished files.

### 1. Map the exam before writing cards

Start with the [official ACSM-CPT Exam Content Outline](https://acsm.org/wp-content/uploads/2024/12/ACSM-Certified-Personal-Trainer-Exam-Content-Outline.pdf). Check the [ACSM certification page](https://acsm.org/certification/get-certified/personal-trainer/) for a newer version. The baseline outline, effective July 10, 2025, has 18 tasks and 170 lettered knowledge and skill statements by my count. If the outline has changed, use the current version and record its effective date.

Give every statement a stable ID such as `I.E.K.c` for Domain I, Task E, Knowledge, item c. Break broad statements into their individual testable concepts. For example, a statement listing 22 movement and anatomy terms needs coverage of all 22. A single card tagged to that statement does not establish coverage.

Use these approximate card budgets. Adjust them where the content warrants it.

| Domain | Target cards |
|---|---:|
| Client consultation and assessment | 300 |
| Exercise programming and implementation | 420 |
| Exercise leadership, client education, and engagement | 160 |
| Legal and professional responsibilities | 120 |

### 2. Write cards that test useful knowledge

- Give each card one clear question and one independently gradable answer. Put the short answer first on the back. Add a brief rationale when it helps explain a decision or distinguish two plausible answers.
- Match the prompt to the skill. Use direct recall for terminology, worked problems for calculations, and short client scenarios for choosing an assessment, adjusting a program, making a referral, or responding to a coaching problem. Give every application or synthesis task at least one scenario.
- Make calculations specific enough to solve. For example, “A client’s resting heart rate is 60 bpm and maximum heart rate is 180 bpm. What is the target at 60% of heart-rate reserve?” The back should show **132 bpm** and the arithmetic, `60 + 0.60 × (180 − 60) = 132`.
- Write original prompts. Use current, authoritative sources for the answers and attach a verifiable source locator to each card. The exam outline establishes **what to cover**. For numerical thresholds, screening decisions, and exercise prescriptions, cite the guideline section, table, or page that supports the **answer itself**. Flag anything you cannot verify as a gap. Never invent a citation.
- Tag each card with its domain, objective ID or IDs, and card type. Reuse a card across objectives when it genuinely tests both. Avoid padding the count with paraphrases or automatic reverse cards.

### 3. Package and verify the deck

Deliver `ACSM-CPT.apkg`, an editable UTF-8 `ACSM-CPT.tsv`, and `coverage.csv`. The coverage report should map each objective and its component concepts to actual card IDs and flag any partial coverage. Use stable note IDs so later corrections can update the same notes.

Before finishing, verify that the package can be opened, its card count matches the export, and all card IDs in the report exist. Check for blank fields, duplicate questions, arithmetic errors, and scenarios with more than one defensible answer. Manually review a sample from each domain for factual accuracy and correct objective mapping.

Report the final card count by domain, the number of fully covered objectives, and any unresolved gaps. Keep building past the outline and sample-card stage until the deck is ready to import.
