# Frontier ML — Research and Engineering

Start with probability, gradients and simple predictors. Finish by designing an experiment, diagnosing a distributed run and deciding whether a model is worth deploying. The curriculum has **1,116 cards across 250 skills**. Each skill has at least four independently answerable prompts spanning at least three kinds of retrieval. Coding and work-sample topics use short questions about a formula, a prediction, a failure mode or a decision.

In Anki, choose **File → Import** and select the package. The deck name is **Frontier ML — Research and Engineering**. [Anki package](release/Frontier-ML.apkg) · [Editable Anki TSV](release/Frontier-ML.tsv) · [Skill-to-card map](release/coverage.csv)

## First study session

Start with stage 01. The package assigns new-card positions by stage and interleaves skills within each stage. In Anki, use ascending new-card position for the initial pass if your preset randomizes new cards. To focus on one stage, use a filtered deck or the Browser search `deck:"Frontier ML — Research and Engineering" tag:stage::01`. Study due reviews across earlier stages as you advance.

Answer the question on the front before revealing the back. Grade yourself on that one answer. Worked reasoning appears below the answer when it helps.

## Visual math practice

The package includes **360 distinct code-generated figures on 761 cards** across all 12 stages. Every mathematics and statistics card (121) and every calculation card across the deck (187) includes a figure. These groups overlap. Search `tag:medium::figure` in Anki to see all illustrated cards.

| Anki search | What to practice |
| --- | --- |
| `tag:visual::primer` | 50 introductory cards. Read a cell, follow a chance branch, find a slope or locate an interval before moving to the general rule. |
| `tag:visual::question` | 22 chart questions. Use the evidence on the front to locate a masking violation, identify a saddle point or interpret a precision–recall curve. |
| `tag:visual::worked` | 689 cards with a worked illustration after the answer. Examples include the shaded probability of rejecting under an alternative, normalization of attention weights and the cost of retrying until success. |

Each question has one grading target. The [introductory questions](primer-figures.tsv), [chart questions](figure-cards.tsv) and [worked examples](worked-figures.tsv) map card IDs to PNGs and text descriptions. The figures ship inside the package. From this directory, `just figures` reproduces them from the [chart source](plots.py) and the [worked-example renderer and lesson modules](visual_examples.py).

## Curriculum

| Stage | Skills | Cards | Cards with figures | Topics |
| --- | ---: | ---: | ---: | --- |
| 01 · Mathematics and statistics | 22 | 121 | 121 | Softmax derivatives, stable cross-entropy, variance and conditioning. |
| 02 · Classical ML and experiments | 20 | 84 | 77 | Baselines, leakage-resistant splits, calibration and thresholds. |
| 03 · Deep learning and representation | 21 | 88 | 82 | Optimization, neural representations and learning dynamics. |
| 04 · Architectures | 21 | 92 | 82 | Attention, state-space models, multimodal encoders and diffusion. |
| 05 · Data and pretraining | 20 | 86 | 49 | Corpora, tokenization, packing, compute budgets and contamination. |
| 06 · Accelerators and distributed training | 21 | 88 | 54 | Memory, FLOPs, parallel layouts and profiling. |
| 07 · RL and sequential decisions | 20 | 92 | 66 | Bellman targets, advantage estimates, termination and truncation. |
| 08 · Post-training and alignment | 18 | 78 | 41 | PPO, DPO, reward quality and policy evaluation. |
| 09 · Inference, retrieval and agents | 21 | 90 | 52 | KV caches, scheduling, retrieval, decoding and tool use. |
| 10 · Evaluation and interpretability | 20 | 86 | 47 | Paired evaluations, uncertainty, mechanistic claims and grading. |
| 11 · Coding and production engineering | 21 | 87 | 36 | Algorithms, reproducibility, distributed failures and rollback. |
| 12 · Frontier methods and research design | 25 | 124 | 54 | Research design, training investment, oversight and launch decisions. |

The sequence and skill map are original. Public lab material informed the interview and work-sample choices. Interview content varies by team. [OpenAI interview guide](https://openai.com/interview-guide/) · [Anthropic careers](https://www.anthropic.com/careers) · [Google DeepMind careers](https://deepmind.google/careers/)

## Targeted review

Use `tag:type::calculation` for short numerical questions, `tag:type::diagnosis` for debugging, or `tag:type::decision` for tradeoffs. To review one skill, search for its objective identifier from the coverage map, for example `tag:skill::lossmask`.

The ten standalone [Python exercises](practice/exercises.py) and their [worked solutions](practice/solutions.py) are optional companions for use outside Anki. From the practice directory, copy the starter to `answers.py` and run `python3 check.py answers.py cross_entropy` to check that function.

## Edit, rebuild and verify

`cards.tsv` and `components.csv` are the human-editable authoring sources. Preserve existing card IDs to retain note identity on revisions. The generated TSV in `release/` is an Anki update file with GUIDs. Import the package first to install the note type. To update from text, use the generated Anki TSV and check the field mapping in the import preview.

From this directory with `just` and `uv` installed, choose a fresh build location:

```bash
just build release-next
just test release-next
```

The verifier opens the package in a temporary Anki collection, checks rendered questions and answers, edits every answer, then imports the TSV and checks that it restores every note while preserving its identity. The test recipe also runs the reference implementations against the editor fixtures. [Authoring cards](cards.tsv) · [Curriculum map](components.csv)
