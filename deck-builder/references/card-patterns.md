# Writing cards that survive a shuffle

| Source or draft | Study cue | Answer and rationale |
| --- | --- | --- |
| “Evaporation cools the liquid because the faster molecules preferentially escape.” | Why does evaporation lower the temperature of the remaining liquid? | Faster molecules preferentially escape. The mechanism is the graded answer. |
| “Things expand when heated.” The source specifically describes a metal rod under free expansion. | Under free expansion, how does heating a metal rod affect its length? | Its length increases. Keep the condition on the front. |
| “What does *bank* mean?” | In “she sat on the river bank,” what does *bank* refer to? | The land beside the river. For production, supply context that singles out the desired word or accept alternatives. |
| “TCP vs UDP?” | Which transport protocol in this pair provides ordered delivery of a byte stream? | TCP. Split unrelated differences into separate cards when those distinctions matter. |

**Cloze.** In `A lunar eclipse occurs when {{c1::Earth}} lies between the Sun and the {{c2::Moon}}.` each card shows a different part of the geometry. Check each visible word for accidental giveaways. Use a single index for an inseparable expression such as a value and its unit. Keep explanations below the reveal.

**Quantities and equations.** Specify the conditions, units, and the variable being solved for. Write Anki MathJax as `\(v = d/t\)` in a field and double the backslash in JSON. Put one short worked example on the answer side when it clarifies grading.

**Images and sound.** Choose media that supplies evidence for the question. Crop to the relevant region while preserving orientation and scale. For a label test, use a genuinely masked prompt image and show the labeled original on reveal. A caption, alt text, or filename visible during review can give away the answer. For editable native image occlusion, use Anki's Image Occlusion editor or a tested exporter for its specific note schema.

**Mathematical figures.** Generate quantitative plots from code and stated data. Use the point cloud, curve, matrix or graph as evidence for one inference. Give axes units, distinguish series without relying on color alone, and describe the available observations in alt text. Keep enough context for a phone screen. Verify the plotted answer from the underlying numbers and check the media in a real package import.

For a quantitative curriculum, walk the objectives in every stage, including mathematics embedded in applied and debugging questions. Identify what a beginner must be able to see, such as probability as area, a derivative as a slope or a waiting-time distribution as a long tail. When the representation is itself unfamiliar, start with a short question about reading one axis, branch, cell or interval. Put unsolved visual evidence on the front when interpreting it is the target. Put a labeled, worked diagram on the back when it would reveal a formula or decision. Reuse a diagram only when its quantities and relationships directly support each linked question. Report both distinct figures and cards with figures so repeated assets do not inflate the apparent breadth of coverage.

**Revision.** Read a card without its deck title or neighboring cards. If several answers fit, narrow the cue or enumerate accepted synonyms. Compare with the source after rewriting so an easier question still tests the intended knowledge.

## Choosing a second cue

| What should the learner be able to do? | Make this choice |
| --- | --- |
| Retrieve both members of a useful, unambiguous pair | Use a reversed note. Anki schedules its two cards separately. Preview both directions, including any audio. |
| Understand a spoken Mandarin word and produce it from English | For listening, play the Mandarin audio on the front. For production, disambiguate the English sense on the front and put the spoken model on the back. Decide whether spoken form, written characters or both count for this task. |
| Apply a principle when different evidence is present | Give the new case its own card and answer. Include cases where a familiar cue is present but the usual decision would be wrong. |
| Retrieve the same answer despite incidental wording | Draft a small set of alternative prompts during authoring. The manifest’s `varied` type can show one of them per presentation. All share one grade, so use comparable difficulty and one answer key. |
| Know a precise phrase, threshold, formula or rule | Keep the target stable. Supply units, population, time period and exceptions needed to grade it. A changed threshold or a reversed inequality can change the answer. |

**Review an AI draft.** Hide the model answer and solve each version independently. Compare the required answer, acceptable synonyms, units, polarity and scope with the source. Remove any version that supplies the answer or makes another answer equally defensible. When one version adds a calculation, an exception or a new decision, give it an independent card. For a yes/no judgment, ask what observation, rule or mechanism decides the case when that is the skill being tested. Reserve a fresh example to check transfer after a delay.

Butler’s passage experiments found a benefit from retrieval practice and no reliable extra benefit from rewording the same questions. A later set of experiments found better transfer when students retrieved and applied the same concept across different examples. Webb’s word-pair study found that the direction of practice affected which aspects of vocabulary students learned. These results support authoring for the desired performance. They do not establish a benefit for live AI rewriting during Anki review. [Butler, 2010](https://doi.org/10.1037/a0019902) · [Butler et al., 2017](https://pubmed.ncbi.nlm.nih.gov/29265856/) · [Webb, 2009](https://doi.org/10.1177/0033688209343854)
