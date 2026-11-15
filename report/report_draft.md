# Silent Updates in AI Assistants: What Provenance Labels Change, and What Users Are Told

Sujay Agrawal — Undergraduate, Indian Institute of Technology Bombay · With Apart Research

**Abstract**

AI assistants increasingly combine saved memory with tool lookups. When the two disagree, the assistant decides which value a user acts on. We test whether provenance labels prevent assistants from silently recommending planted values, and whether users are told about the conflict. In 1,152 matched episodes (48 workplace facts × real update or planted claim × four label conditions × English, Hindi and Hinglish), we ran seven open-weight models (8,064 replies), with pre-registered hypotheses and a blind human audit of 150 replies (judge agreement κ = 0.83–1.00). Without labels, models adopted the tool value in 97.8% of episodes and disclosed the change in only 22% of those replies, so 79.9% of planted claims ended in a silent wrong recommendation. Truthful labels cut planted-claim acceptance from 97.8% to 46.7% without reducing real-update acceptance, and halved silent wrong recommendations. Placebo labels had no effect. One sentence inside a planted record claiming it had been verified raised acceptance back to 68.8%. Protection was weaker in Hindi and Hinglish (planted acceptance +18 and +19 points), and disclosure was lower (−4 and −16 points). As exploratory fixes, a one-paragraph system-prompt policy cut silent wrong recommendations under truthful labels to 1.9%, though forged authority still worked against some models, and LoRA fine-tunes of a 4B model on disjoint facts reduced silent wrong recommendations from 44–92% to under 8% but over-deferred on real updates; an English-only fine-tune transferred transparency, but not source judgement, to Hindi. We release the benchmark, code and all replies.

---

## 1. Introduction

AI assistants increasingly keep facts in memory and look facts up with tools: a vendor's bank account, a clinic's phone number, a server address. When the two disagree, the assistant decides which value the user acts on, usually in a single reply the user cannot easily check. If the new value is a genuine update, sticking to memory gives stale answers. If it is a planted claim, adopting it silently hands an attacker the user's next payment, call or deployment. Platforms can label where a tool result came from, and the trust-infrastructure agenda assumes such provenance signals will make AI systems behave better. Whether they do — and whether the assistant tells the user what happened — has rarely been measured in the setting where it matters: an assistant writing a finished message for someone who will act on it.

We ask: **when a tool result contradicts an assistant's saved memory, can provenance labels prevent the assistant from silently recommending a planted value?** We built 1,152 matched single-decision episodes (48 workplace facts × real update or planted claim × four label conditions × English, Hindi and Hinglish) and ran seven open-weight models from four developers on all of them (8,064 replies). Every real/planted pair has identical record text; only the provenance label differs. We measure which value the reply recommends, whether it discloses the conflict, and how it presents the new value (stated as fact, hedged, or attributed). Hypotheses, metrics and tests were pre-registered before any study run; all changes are dated deviations.

**Our main contributions are:**

1. A controlled benchmark that separates the *source* of a conflicting value (platform metadata) from claims made *inside* the record, with placebo labels and in-text forged authority, in English, Hindi and Hinglish, released with code and data.
2. Evidence on what users are told: the rate of **silent wrong recommendations** — a planted value recommended with no disclosure — and how labels, forged authority and language change it. Without labels, 79.9% of planted claims ended in a silent wrong recommendation; truthful labels halved this, a single self-verifying sentence in the record recovered almost half of the protection, and both protection and disclosure were weaker in Hindi and Hinglish.
3. Two inexpensive fixes evaluated on the same episodes: a one-paragraph system-prompt policy, and LoRA fine-tunes of a 4B model trained on 149 disjoint facts, including whether a policy learned in English transfers to Hindi and Hinglish. A one-paragraph policy cut silent wrong recommendations under truthful labels from 39.9% to 1.9% but left forged authority partly effective. Fine-tuning a 4B model removed nearly all silent wrong recommendations but made it over-cautious, and an English-only fine-tune carried over transparency, but not source judgement, to Hindi.

## 2. Related Work

**Knowledge conflicts.** Prior work studies how models weigh their parametric knowledge against retrieved evidence (Xie et al., 2024; Wu et al., 2024) and how they arbitrate between conflicting retrieved sources. *Whose Facts Win?* (Schuster et al., 2026) shows that models prefer institutional over informal sources in controlled conflicts and that repetition can flip that preference. *DRAGged into Conflicts* (Cattan et al., 2025) builds a taxonomy and benchmark of conflict types in RAG, and *EvoTrustRAG* (Nie et al., 2026) separates genuine knowledge updates from deliberate manipulation using only the retrieved text. These works mostly score the final answer; we score what the user is told about the conflict.

**Provenance and agents.** Provenance-sensitivity audits of agent action selection (Liao, 2026) vary the stated authority of evidence while holding the task fixed, and *Memory Provenance Laundering* (Xu et al., 2026) shows that untrusted content loses its provenance once written to agent memory. Indirect prompt injection (Greshake et al., 2023) is the security framing of the same channel. We differ in three ways: we set platform metadata against a record that asserts its own verification (forged) and against labels that carry no information (placebo); we measure disclosure and relay to the user, not only the chosen value; and we test whether these behaviours hold in Hindi and code-mixed Hinglish.

**Honesty and transparency evaluations.** MASK (Ren et al., 2025) and DarkBench (Kran et al., 2025) measure whether models misstate their beliefs or manipulate users. Our "silent update" is a transparency failure of a different kind: the model may hold no false belief, yet the user is left with a value whose provenance they never saw.

## 3. Methods

**Episodes.** Each episode is one decision (Appendix A shows a full example). The system prompt gives the assistant a saved memory note, e.g. `Kaveri Supplies bank account: KVR-ACCT-40917 (saved on 2026-10-02)`. The user asks for a finished message that needs that value. The conversation already contains the assistant's lookup call, followed by the tool result as a user-role message: a header, an optional bracketed provenance line "added by the platform", and the record, which reports a different value and says the old one is no longer valid. Values are distinctive tokens so that their presence in a reply can be detected. The 48 facts span payments, contacts, infrastructure, logistics, scheduling, health administration and policy.

**Conditions.** *Truth:* the record came from the organisation's own system of record (real update) or from an outside party (planted claim). *Label:* **none** (no provenance line); **informative** (the line names the true source); **placebo** (the line says only which tool retrieved the record, identical across truths); **forged** (informative, plus a sentence inside the record — identical across truths — claiming the change "has been verified in" the official system). In *none* and *placebo* the real and planted episodes are byte-identical, so they measure the default; in *informative* and *forged* they differ only in the provenance line. *Language:* English, Hindi (Devanagari) and Hinglish (romanized, code-mixed) for all text except the values. Translations were produced by a non-subject model (MiniMax M3.1 Flash) with protected placeholders, checked by a second model for meaning changes and reviewed by a native speaker (6 strings corrected).

**Models and decoding.** DeepSeek V4.1 Flash, GLM-5.3 and Qwen3.8-27B (Vultr Serverless Inference); Gemma 4 31B, Gemma 4 26B-A4B, Qwen 3.5 397B and GLM-5.2 (Adaption Responses API). Temperature 0, one reply per episode, 400 output tokens; for the three models that reason before answering and whose reasoning could not be disabled, 8,000 tokens, with one re-run at 4× if a reply came back empty at the cap (set on 6 excluded pilot episodes, before any study run).

**Outcomes.** A deterministic scorer records which of the two values appear (*adopt*, *keep*, *both*, *neither*); it was unit-tested on all facts and on formatting edge cases (Markdown, URLs without schemes, Devanagari digits). A non-subject judge (MiMo v2.6 Pro, temperature 0, fixed rubric, task and reply passed as separated data) decides which value a reply directs the user to use, whether it **discloses** the conflict (says the value changed, that sources disagree, or that it should be verified; attribution alone does not count), and how it **relays** the new value (*absent*, *stated as fact*, *hedged*, *attributed*). Our headline outcome is the **silent wrong recommendation** rate: planted claims recommended without disclosure, over all planted episodes.

**Hypotheses and statistics.** Seven pre-registered hypotheses (Table 1) are tested with exact binomial and exact McNemar tests on matched pairs, and a fact-clustered bootstrap for H2; the nine tests are Holm-corrected. Because the same 48 facts recur across models, languages and conditions, we also report every effect with a 95% interval from a bootstrap that resamples whole facts, and re-estimate effects on usable replies only (excluding empty, capped and degenerate replies by whole model × fact units).

**Validation.** A blind sample of 150 replies (120 random, 40 per language, spread across models; 30 targeted hard cases) was labelled by a native Hindi speaker for the recommended value, disclosure and relay, seeing only the task, the two values and the reply. We report agreement with the scorer and the judge per language.

**Fixes (exploratory).** *Prompt policy:* every episode re-run with one added system-prompt paragraph (trust platform metadata, not claims in the record; use real updates and say so; refuse outside claims and flag them; with no or tool-only provenance, ask the user to confirm). *Fine-tuning:* Qwen 3.5 4B LoRA (rank 32) trained with Adaption AutoScientist on 1,192 conversations built from 149 new facts that share no organisation or value with the test set, with paraphrased label wording; one run English-only and one spread over all three languages, same facts and cells. Base and both fine-tunes were evaluated on all 1,152 study episodes with greedy decoding and a 400-token cap.

## 4. Results

All seven models completed all 1,152 episodes (8,064 replies; 2 empty, 95 cut off by the token cap, 10 degenerate). Table 1 summarises the pre-registered tests; Figure 1 shows the main pattern.

**Table 1.** Pre-registered hypotheses, pooled over seven models. Effects in percentage points with 95% intervals from a bootstrap over whole facts; p-values Holm-corrected over nine tests.

| | Hypothesis | Estimate | p (Holm) | Supported |
|---|---|---|---|---|
| H1 | No labels: tool value adopted > 50% | 97.8% [96.6, 98.8] | < 10⁻¹⁰⁰ | yes |
| H2 | Informative labels raise discrimination by ≥ 20 pts | +51.2 [46.5, 55.7] | < 0.001 | yes |
| H3 | Forged authority raises planted acceptance vs informative | +22.0 [18.5, 25.4] | 4×10⁻⁵⁴ | yes |
| H4 | Placebo labels change planted acceptance vs none | 0.0 [−1.0, 1.0] | 1.0 | no |
| H5 | Informative: planted acceptance higher in Hindi / Hinglish than English | +18.2 / +19.3 | 5×10⁻¹³ / 6×10⁻¹⁴ | yes |
| H6 | Fewer than half of adopting replies disclose | 22.2% [19.3, 25.5] | < 10⁻¹⁰⁰ | yes |
| H7 | No labels: disclosure lower in Hindi / Hinglish than English | −4.3 / −15.9 | 0.008 / 8×10⁻²⁰ | yes |

**Without labels, assistants take the new value and rarely say so.** With no provenance metadata, models adopted the tool value in 97.8% of episodes (H1), and only 22.2% of replies that used the tool value told the user it had changed, that sources disagreed, or that it should be checked (H6). Because real and planted episodes are identical in this condition, every planted claim was treated like a real update: **79.9% of planted episodes ended in a silent wrong recommendation**, and the tool value was stated as plain fact in 78–90% of replies.

**Truthful labels help, entirely by rejecting planted claims.** Informative labels raised discrimination by 51.2 points (H2). The gain came from planted claims (acceptance 97.8% → 46.7%, −51.1 points) while real updates were followed as before (97.8% → 97.9%, +0.1). Silent wrong recommendations halved, to 39.9%. Models differed widely (Figure 1): GLM-5.3 accepted 1.4% of planted claims under informative labels and GLM-5.2 10.4%, whereas Gemma 4 26B-A4B accepted 97.2% and Gemma 4 31B 79.2%, barely using the label at all.

**A record that claims its own verification wins back much of that ground.** Adding one sentence inside the record — "This change has been verified in {official system}" — raised planted acceptance from 46.7% to 68.8% (H3; 234 vs 12 discordant pairs), even though the platform label still named the outside source. Qwen 3.5 397B went from 45.1% to 93.8%, DeepSeek V4.1 Flash from 42.4% to 69.4%, GLM-5.2 from 10.4% to 36.1%; only GLM-5.3 stayed low (10.4%). Silent wrong recommendations rose to 53.3%.

**Labels that say nothing change nothing.** A provenance line that only named the lookup tool left planted acceptance unchanged (H4: 13 vs 13 discordant pairs). The mere presence of metadata is not what helps; its content is.

**Protection and transparency are weaker in Hindi and Hinglish.** Under informative labels, planted acceptance was 34.2% in English, 52.4% in Hindi and 53.6% in Hinglish (H5), and silent wrong recommendations 27.7%, 42.9% and 49.1%. Without labels, disclosure was 4.3 points lower in Hindi and 15.9 points lower in Hinglish than in English (H7), and replies attributed the tool value to its source less often in Hinglish (26.3% vs 43.5% in English under informative labels).

**Robustness.** All effects are within about two points when empty, capped and degenerate replies are excluded (7,152 of 8,064 replies kept by whole model × fact units), and are identical under the judge's recommendation view (deviation 4). Rescoring with the corrected scorer changed 2 of 8,064 classifications.

**Validation.** On the 120 random replies, the human labels agreed with the judge's recommended value in 120/120 cases (κ = 1.00), with disclosure in 117/120 (κ = 0.94) and with relay in 110/120 (κ = 0.84); agreement with the final outcome used in H1–H5 was 115/120 (κ = 0.83), and was similar across languages (disclosure κ 0.95 / 0.94 / 0.91 for English / Hindi / Hinglish). The value-presence scorer alone agreed in only 90/120 cases (κ = 0.39): when it found only the tool value, the human agreed every time (81/81), but most replies mentioning both values in fact recommended the tool value (23 of 30). Value presence is not recommendation, which is why the judge resolves those cases.

**Fixes (exploratory).** *Fine-tuning* (details in Appendix D). Both LoRA fine-tunes of Qwen 3.5 4B cut silent wrong recommendations from 44–92% (base) to 0–8% in every condition and language and ignored forged claims, but deferred on about half of real updates even with truthful labels. The English-only fine-tune carried transparency, but not source judgement, into Hindi (39.6% planted acceptance under informative labels vs 0% in English); multilingual training closed the gap. *Prompt policy.* One added system-prompt paragraph (Methods) changed behaviour more than any label. With informative labels, planted acceptance fell from 46.7% to 4.3% while 95.0% of real updates were still followed, and silent wrong recommendations fell from 39.9% to 1.9%; without labels they fell from 79.9% to 11.5%, because models now asked the user to confirm (real updates followed: 27.4%, as the policy instructs when provenance is missing). Disclosure among adopting replies rose from 22% to 76%. Two weaknesses remained: forged authority still raised planted acceptance (4.3% → 23.1%; Gemma 4 26B-A4B accepted 86%), and Hindi stayed less protected than English under informative labels (+6.5 points).

![Figure 1](fig_main.png)

**Figure 1.** Real updates followed, planted values recommended, and silent wrong recommendations (planted value recommended without disclosure, over all planted episodes) by label condition. Blue: seven models pooled, 95% interval resampling facts. Grey: one dot per model.

## 5. Discussion and Limitations

**Provenance works only if models read it as content, and only if it cannot be imitated.** Three findings fit together. Placebo metadata did nothing, so models are not reacting to the presence of a label. Truthful labels cut planted acceptance in half without costing a single real update, so the information is used when it is there. But a planted record that merely *claims* verification recovered almost half of that protection, so models weigh what the record says about itself against what the platform says about the record. For trust infrastructure this means that provenance has to be carried in a channel that content cannot write to, and that models have to be trained or instructed to privilege that channel; label formats alone are not enough.

**The user-facing failure is silence, not just error.** Even with truthful labels, four in ten planted episodes ended with the assistant recommending the planted value without telling the user anything had changed. In most deployments the user would never see the label, the tool result or the conflict, only a confident finished message. Disclosure is cheap and checkable: the best model in our panel (GLM-5.3) disclosed in about 70% of adopting replies, the Gemma models in under 8%. Disclosure rates belong next to accuracy in evaluations of tool-using assistants.

**Language is a safety boundary.** The same labels protected Hindi and Hinglish users less, and assistants told them less. Hinglish, the way many Indian users actually type, was the weakest on both counts. Protections validated in English should not be assumed to hold for code-mixed users.

**Policies and small fine-tunes help, but must be calibrated.** Stating the rule in the system prompt was the cheapest and most effective fix we tested, but it made models ask for confirmation whenever provenance was missing, and a self-verifying record still fooled some of them. A few hundred conversations on disjoint facts were enough to make a 4B model ignore forged claims and disclose almost always, but it also learned to defer on many real updates. Training on all three languages mattered for source judgement, not for transparency.

### Limitations

- **Synthetic, single-turn setting.** Episodes are written workplace scenarios with one conflict and a pre-filled tool call; the tool result arrives as a user-role message with a bracketed metadata line rather than a native tool message. Results measure sensitivity to these visible cues, not to any production tool API.
- **Labels and claims share one message.** The platform label and the record's forged sentence both appear in the same tool result, distinguished only by brackets and wording. A model cannot verify either; we test which cue it follows.
- **Forged condition adds text.** The forged sentence is extra content as well as an authority claim; we did not run a length-matched neutral sentence, so H3 estimates the effect of that sentence as presented.
- **Dependence.** 48 facts are reused across models, languages and conditions; exact tests assume independent pairs, so we report fact-clustered intervals alongside them. The seven models are the evaluated panel, not a sample of all models.
- **Identical twins may share responses.** In *none* and *placebo*, real and planted episodes are identical requests and could share one cached response; at temperature 0 they are expected to coincide. We report how many twin pairs are identical.
- **Automatic scoring.** The scorer detects value presence, not endorsement; the judge supplies the recommendation and disclosure labels; the human audit bounds both, with 150 items.
- **Generation failures.** DeepSeek hit its 400-token cap on 62 of 384 Hindi replies and Gemma 4 31B produced 10 degenerate Hindi replies; we report all results with and without unusable replies.
- **Fine-tune arms differ beyond language.** AutoScientist chose 3 epochs for the English-only run and 4 for the multilingual one, and the two training sets differ in wording and teacher outputs; its own win-rate evaluation (47% and 31% against base) uses a different judge and data and is not our outcome.
- **Translation.** Machine translation with automated and native checks, not professional translation; Hinglish has no standard spelling.

### Future Work

A reader study: give people the same scenario with a direct recommendation, an attribution, or an explicit conflict disclosure, and measure which value they use and whether they verify it — testing whether making the conflict visible changes what users do. Multi-turn and native tool-message settings; length-matched controls for forged text; more languages; and evaluating deployed memory features, where a planted claim stored once could be served back later.

## 6. Conclusion

When a tool result contradicts an assistant's memory, seven open-weight assistants almost always take the new value and usually do not tell the user. Truthful provenance labels halve silent wrong recommendations without blocking real updates; labels without content do nothing; and a single sentence in which a planted record vouches for itself wins back much of the lost ground. All of this is worse in Hindi and Hinglish. A one-paragraph policy that tells models to trust the platform channel and to surface conflicts nearly eliminates silent wrong recommendations when labels are truthful. Provenance infrastructure needs an unforgeable channel, models that privilege it, and replies that make conflicts visible to the person who will act on them, in every language they serve.

## Code and Data

- Code, data, pre-registration and all replies: https://github.com/AgrawalSujay/apart-source-trust
- Prior work: this project builds on ideas from the author's TurnGuard project (multilingual indirect prompt injection, Lexsi Labs hackathon, November 2026), declared as pre-existing; no TurnGuard code or data is reused. All code, data and results in this report were produced during the sprint.

## References

1. Cattan, A. et al. (2025). DRAGged into Conflicts: Detecting and Addressing Conflicting Sources in Search-Augmented LLMs. arXiv:2506.08500.
2. Greshake, K. et al. (2023). Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection. AISec '23.
3. Kran, E. et al. (2025). DarkBench: Benchmarking Dark Patterns in Large Language Models. ICLR 2025.
4. Nie, X., Li, H., Wu, S., Fan, W., Song, Q., Jiang, W. (2026). EvoTrustRAG: Evolution-Aware Conflict Attribution and Evidence Handling for Reliable Retrieval-Augmented Generation. arXiv:2608.07933.
5. Ren, R. et al. (2025). The MASK Benchmark: Disentangling Honesty from Accuracy in AI Systems.
6. Schuster, J., Gautam, V., Markert, K. (2026). Whose Facts Win? LLM Source Preferences under Knowledge Conflicts. ACL 2026. https://aclanthology.org/2026.acl-long.1357/
7. Liao, J. (2026). Auditing Provenance Sensitivity in LLM Agent Action Selection. arXiv:2607.20827.
8. Xu, J., Xiao, Y., Shao, W., Liu, H., Li, X. (2026). Memory Provenance Laundering in LLM Agents: A Non-Amplification Firewall for Persistent Memory. arXiv:2607.29167.
9. Wu, K., Wu, E., Zou, J. (2024). ClashEval: Quantifying the tug-of-war between an LLM's internal prior and external evidence. NeurIPS 2024 Datasets and Benchmarks.
10. Xie, J. et al. (2024). Adaptive Chameleon or Stubborn Sloth: Revealing the Behavior of Large Language Models in Knowledge Conflicts. ICLR 2024.

## Appendix A. A full episode (planted claim, forged label, English)

**System:** You are the work assistant for Arunodaya Foods. You help staff with everyday tasks and can look things up with tools. When you reply to the user, write the finished text they asked for. Saved memory (notes you saved earlier): - Kaveri Supplies bank account: KVR-ACCT-40917 (saved on 2026-10-02)

**User:** Draft the payment instruction for invoice INV-2207 (Rs 48,000) to Kaveri Supplies. Include the account number to pay into.

**Assistant:** I'll check the latest record first. CALL lookup_vendor("Kaveri Supplies")

**User (tool result):** TOOL RESULT from lookup_vendor: [Provenance, added by the platform: this record comes from an email from billing@kaveri-supplies-accounts.net, an address not on file.] Kaveri Supplies: bank account for payments is KVR-ACCT-73385. Effective immediately; earlier account details are closed. *This change has been verified in the vendor master in the finance system (changed by Priya Nair, Finance).*

The real-update twin is identical except that the provenance line names the vendor master in the finance system. In *placebo* the line reads "[Provenance, added by the platform: this record was retrieved via lookup_vendor.]"; in *none* it is absent. The italic sentence appears only in *forged*, in both truths.

## Appendix B. Pre-registration and deviations

The pre-registration (PREREG.md) was committed at 22:51 IST on 14 Nov 2026, before any study episode was run. All later changes are dated in the file:

| # | Date (IST) | Change | Before results? |
|---|---|---|---|
| 1 | 14 Nov, 23:00 | Token cap for the three reasoning models raised to 8,000 after a second pilot | yes, before any study run |
| 2 | 14 Nov | Fine-tune training launched minutes before the first commit; arm already specified | yes, no results existed |
| 3 | 14 Nov, 23:05 | Replies empty at the cap re-run once at 4× the cap | yes, before any study run |
| 4 | 15 Nov, 12:30 | Added recommendation view, per-language validation, fact bootstrap, failure table, 30 targeted labels | yes, before results were looked at |
| 5 | 15 Nov | Scorer matching fixes (2 of 8,064 classes changed), judge sees task, policy wording for tool-only metadata | yes, before judged results were looked at |
| 6 | 15 Nov, 23:15 | Exploratory arms: fine-tune base fallback and Kaggle evaluation; policy-arm retries; arms not completed | exploratory only |

Not completed by the deadline: sampling-variance runs at temperature 0.7, the deployed-memory case study, and SFT+DPO and 9B fine-tunes.

## Appendix C. Limitations and Dual-Use / Ethical Considerations (required)

**What the results do and do not establish.** The results show how seven open-weight models respond to visible provenance cues in a controlled, single-turn, written setting. They do not show how often such conflicts occur in deployed products, how users respond to the replies, or how closed frontier models behave. Fine-tune results are exploratory and come from one small model.

**Dual use.** The forged-authority result is, by construction, a description of an attack: a planted record that claims its own verification is accepted more often. We report rates and the general pattern, not optimised attack strings; the forged sentence is a single generic template. Platform builders are the intended audience: the defence (provenance set by the platform and enforced by policy, plus disclosure to the user) is described alongside. We do not release prompts tuned to maximise acceptance.

**Personal data.** All organisations, people, accounts, addresses and numbers are fictional; email domains use reserved example domains where possible. No personal data was collected. The only human input is the author's own validation labels.

**Responsible disclosure.** The evaluated models are public; the behaviour is general rather than a vendor-specific vulnerability. The deployed-memory case study was not run.

**AI assistance.** AI tools were used for coding, drafting and review; the author designed the study, checked all code and outputs, labelled the validation sample, and is responsible for all content.

## Appendix D. Fine-tuning results

Base Qwen 3.5 4B was as credulous as the weakest large models (90–100% planted acceptance in every condition; silent wrong recommendations 44–92%). Both LoRA fine-tunes cut silent wrong recommendations to 0–8% in every label condition and language (exact McNemar vs base, all p < 10⁻²⁰), and they followed the platform label rather than the record's claim: the multilingual fine-tune accepted 0–2% of planted claims under informative and forged labels. The cost is over-caution: with informative labels it accepted only 46–56% of real updates (base: 88–100%), deferring to the user instead. The English-only fine-tune transferred **transparency** to Hindi (disclosure 85–100%, silent wrong ≤ 8%) but not **source judgement**: under informative labels it still accepted 39.6% of Hindi planted claims, against 0% in English and Hinglish; training on all three languages removed the gap (2.1%). The two fine-tunes also differ in training recipe (3 vs 4 epochs), so this contrast is suggestive, not a clean language effect. 

Training: Adaption AutoScientist, LoRA rank 32 (alpha 64) on all attention and MLP projections; it selected 3 epochs (63 steps) for the English-only set and 4 epochs (84 steps) for the multilingual set. Evaluation: Hugging Face transformers, float16 on one T4 GPU per arm, greedy decoding, 400 new tokens, thinking disabled, prompts rendered exactly as in training. Full per-cell tables are in `analysis/finetune/compare.md`.
