# Fine-tune comparison (exploratory)

| Training arm | Epochs | Optimizer steps |
|---|---:|---:|
| qwen3.5-4b-ft-en | 3 | 63 |
| qwen3.5-4b-ft-multi | 4 | 84 |

The checkpoints differ in the selected training recipe as well as the training language.
The comparison estimates the effect of each complete checkpoint and cannot isolate a recipe-matched language effect.

Acceptance uses the study's final adopt outcome. Silent wrong recommendation uses the
judge's recommendation and disclosure labels. Each percentage uses eligible judged rows in its displayed
cell. A missing denominator is shown as an em dash.

| Arm | Expected | Valid judged | Unresolved | Missing |
|---|---:|---:|---:|---:|
| qwen3.5-4b-base | 1152 | 1152 | 0 | 0 |
| qwen3.5-4b-ft-en | 1152 | 1152 | 0 | 0 |
| qwen3.5-4b-ft-multi | 1152 | 1152 | 0 | 0 |

## Rates by label, truth and language

| Arm | Label | Truth | Language | Judged n | Real-update acceptance | Planted-claim acceptance | Silent wrong recommendation | Deferral | Disclosure |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| qwen3.5-4b-base | none | real | en | 48 | 100.0% | — | — | 0.0% | 10.4% |
| qwen3.5-4b-base | none | real | hi | 48 | 91.7% | — | — | 0.0% | 25.0% |
| qwen3.5-4b-base | none | real | hinglish | 48 | 97.9% | — | — | 2.1% | 10.4% |
| qwen3.5-4b-base | none | planted | en | 48 | — | 100.0% | 91.7% | 0.0% | 8.3% |
| qwen3.5-4b-base | none | planted | hi | 48 | — | 91.7% | 72.9% | 0.0% | 22.9% |
| qwen3.5-4b-base | none | planted | hinglish | 48 | — | 97.9% | 87.5% | 2.1% | 10.4% |
| qwen3.5-4b-base | informative | real | en | 48 | 100.0% | — | — | 0.0% | 10.4% |
| qwen3.5-4b-base | informative | real | hi | 48 | 87.5% | — | — | 8.3% | 14.6% |
| qwen3.5-4b-base | informative | real | hinglish | 48 | 95.8% | — | — | 0.0% | 10.4% |
| qwen3.5-4b-base | informative | planted | en | 48 | — | 100.0% | 83.3% | 0.0% | 16.7% |
| qwen3.5-4b-base | informative | planted | hi | 48 | — | 89.6% | 75.0% | 4.2% | 14.6% |
| qwen3.5-4b-base | informative | planted | hinglish | 48 | — | 91.7% | 79.2% | 2.1% | 14.6% |
| qwen3.5-4b-base | placebo | real | en | 48 | 97.9% | — | — | 0.0% | 14.6% |
| qwen3.5-4b-base | placebo | real | hi | 48 | 91.7% | — | — | 4.2% | 12.5% |
| qwen3.5-4b-base | placebo | real | hinglish | 48 | 95.8% | — | — | 0.0% | 12.5% |
| qwen3.5-4b-base | placebo | planted | en | 48 | — | 97.9% | 85.4% | 0.0% | 14.6% |
| qwen3.5-4b-base | placebo | planted | hi | 48 | — | 91.7% | 81.2% | 4.2% | 12.5% |
| qwen3.5-4b-base | placebo | planted | hinglish | 48 | — | 95.8% | 83.3% | 0.0% | 12.5% |
| qwen3.5-4b-base | forged | real | en | 48 | 100.0% | — | — | 0.0% | 29.2% |
| qwen3.5-4b-base | forged | real | hi | 48 | 95.8% | — | — | 0.0% | 43.8% |
| qwen3.5-4b-base | forged | real | hinglish | 48 | 97.9% | — | — | 0.0% | 33.3% |
| qwen3.5-4b-base | forged | planted | en | 48 | — | 100.0% | 60.4% | 0.0% | 39.6% |
| qwen3.5-4b-base | forged | planted | hi | 48 | — | 89.6% | 43.8% | 2.1% | 52.1% |
| qwen3.5-4b-base | forged | planted | hinglish | 48 | — | 95.8% | 60.4% | 0.0% | 39.6% |
| qwen3.5-4b-ft-en | none | real | en | 48 | 4.2% | — | — | 95.8% | 100.0% |
| qwen3.5-4b-ft-en | none | real | hi | 48 | 60.4% | — | — | 29.2% | 93.8% |
| qwen3.5-4b-ft-en | none | real | hinglish | 48 | 72.9% | — | — | 18.8% | 100.0% |
| qwen3.5-4b-ft-en | none | planted | en | 48 | — | 4.2% | 0.0% | 95.8% | 100.0% |
| qwen3.5-4b-ft-en | none | planted | hi | 48 | — | 60.4% | 2.1% | 25.0% | 93.8% |
| qwen3.5-4b-ft-en | none | planted | hinglish | 48 | — | 70.8% | 0.0% | 20.8% | 100.0% |
| qwen3.5-4b-ft-en | informative | real | en | 48 | 54.2% | — | — | 45.8% | 100.0% |
| qwen3.5-4b-ft-en | informative | real | hi | 48 | 81.2% | — | — | 4.2% | 85.4% |
| qwen3.5-4b-ft-en | informative | real | hinglish | 48 | 77.1% | — | — | 6.2% | 100.0% |
| qwen3.5-4b-ft-en | informative | planted | en | 48 | — | 0.0% | 0.0% | 25.0% | 100.0% |
| qwen3.5-4b-ft-en | informative | planted | hi | 48 | — | 39.6% | 6.2% | 14.6% | 85.4% |
| qwen3.5-4b-ft-en | informative | planted | hinglish | 48 | — | 0.0% | 0.0% | 4.2% | 97.9% |
| qwen3.5-4b-ft-en | placebo | real | en | 48 | 8.3% | — | — | 91.7% | 97.9% |
| qwen3.5-4b-ft-en | placebo | real | hi | 48 | 68.8% | — | — | 14.6% | 89.6% |
| qwen3.5-4b-ft-en | placebo | real | hinglish | 48 | 43.8% | — | — | 18.8% | 97.9% |
| qwen3.5-4b-ft-en | placebo | planted | en | 48 | — | 8.3% | 2.1% | 91.7% | 97.9% |
| qwen3.5-4b-ft-en | placebo | planted | hi | 48 | — | 68.8% | 8.3% | 16.7% | 85.4% |
| qwen3.5-4b-ft-en | placebo | planted | hinglish | 48 | — | 43.8% | 0.0% | 16.7% | 97.9% |
| qwen3.5-4b-ft-en | forged | real | en | 48 | 79.2% | — | — | 16.7% | 100.0% |
| qwen3.5-4b-ft-en | forged | real | hi | 48 | 89.6% | — | — | 4.2% | 97.9% |
| qwen3.5-4b-ft-en | forged | real | hinglish | 48 | 85.4% | — | — | 2.1% | 100.0% |
| qwen3.5-4b-ft-en | forged | planted | en | 48 | — | 4.2% | 0.0% | 10.4% | 100.0% |
| qwen3.5-4b-ft-en | forged | planted | hi | 48 | — | 39.6% | 2.1% | 6.2% | 95.8% |
| qwen3.5-4b-ft-en | forged | planted | hinglish | 48 | — | 8.3% | 0.0% | 6.2% | 100.0% |
| qwen3.5-4b-ft-multi | none | real | en | 48 | 0.0% | — | — | 100.0% | 100.0% |
| qwen3.5-4b-ft-multi | none | real | hi | 48 | 0.0% | — | — | 97.9% | 100.0% |
| qwen3.5-4b-ft-multi | none | real | hinglish | 48 | 0.0% | — | — | 97.9% | 100.0% |
| qwen3.5-4b-ft-multi | none | planted | en | 48 | — | 0.0% | 0.0% | 100.0% | 100.0% |
| qwen3.5-4b-ft-multi | none | planted | hi | 48 | — | 0.0% | 0.0% | 97.9% | 100.0% |
| qwen3.5-4b-ft-multi | none | planted | hinglish | 48 | — | 0.0% | 0.0% | 97.9% | 100.0% |
| qwen3.5-4b-ft-multi | informative | real | en | 48 | 56.2% | — | — | 41.7% | 100.0% |
| qwen3.5-4b-ft-multi | informative | real | hi | 48 | 45.8% | — | — | 54.2% | 100.0% |
| qwen3.5-4b-ft-multi | informative | real | hinglish | 48 | 47.9% | — | — | 47.9% | 100.0% |
| qwen3.5-4b-ft-multi | informative | planted | en | 48 | — | 0.0% | 0.0% | 22.9% | 100.0% |
| qwen3.5-4b-ft-multi | informative | planted | hi | 48 | — | 2.1% | 0.0% | 20.8% | 100.0% |
| qwen3.5-4b-ft-multi | informative | planted | hinglish | 48 | — | 0.0% | 0.0% | 4.2% | 100.0% |
| qwen3.5-4b-ft-multi | placebo | real | en | 48 | 2.1% | — | — | 97.9% | 100.0% |
| qwen3.5-4b-ft-multi | placebo | real | hi | 48 | 6.2% | — | — | 93.8% | 100.0% |
| qwen3.5-4b-ft-multi | placebo | real | hinglish | 48 | 0.0% | — | — | 95.8% | 100.0% |
| qwen3.5-4b-ft-multi | placebo | planted | en | 48 | — | 2.1% | 0.0% | 97.9% | 100.0% |
| qwen3.5-4b-ft-multi | placebo | planted | hi | 48 | — | 6.2% | 0.0% | 93.8% | 100.0% |
| qwen3.5-4b-ft-multi | placebo | planted | hinglish | 48 | — | 0.0% | 0.0% | 95.8% | 100.0% |
| qwen3.5-4b-ft-multi | forged | real | en | 48 | 83.3% | — | — | 16.7% | 100.0% |
| qwen3.5-4b-ft-multi | forged | real | hi | 48 | 77.1% | — | — | 22.9% | 100.0% |
| qwen3.5-4b-ft-multi | forged | real | hinglish | 48 | 68.8% | — | — | 27.1% | 100.0% |
| qwen3.5-4b-ft-multi | forged | planted | en | 48 | — | 2.1% | 0.0% | 2.1% | 100.0% |
| qwen3.5-4b-ft-multi | forged | planted | hi | 48 | — | 2.1% | 0.0% | 20.8% | 100.0% |
| qwen3.5-4b-ft-multi | forged | planted | hinglish | 48 | — | 0.0% | 0.0% | 4.2% | 100.0% |

## Exact paired tests on planted episodes

Two-sided exact McNemar tests pair by fact × language within each label. P-values are unadjusted
and exploratory. Reuse of the same facts across languages can make the nominal p-values optimistic.

| Fine-tune vs base | Label | Outcome | Paired n | FT only | Base only | Change (pp) | Exact p |
|---|---|---|---:|---:|---:|---:|---:|
| qwen3.5-4b-ft-en | none | Planted acceptance | 144 | 1 | 75 | -51.4 | 2.038e-21 |
| qwen3.5-4b-ft-en | none | Silent wrong recommendation | 144 | 0 | 120 | -83.3 | 1.505e-36 |
| qwen3.5-4b-ft-en | informative | Planted acceptance | 144 | 1 | 117 | -80.6 | 7.162e-34 |
| qwen3.5-4b-ft-en | informative | Silent wrong recommendation | 144 | 0 | 111 | -77.1 | 7.704e-34 |
| qwen3.5-4b-ft-en | placebo | Planted acceptance | 144 | 1 | 80 | -54.9 | 6.783e-23 |
| qwen3.5-4b-ft-en | placebo | Silent wrong recommendation | 144 | 1 | 116 | -79.9 | 1.42e-33 |
| qwen3.5-4b-ft-en | forged | Planted acceptance | 144 | 1 | 113 | -77.8 | 1.107e-32 |
| qwen3.5-4b-ft-en | forged | Silent wrong recommendation | 144 | 1 | 79 | -54.2 | 1.34e-22 |
| qwen3.5-4b-ft-multi | none | Planted acceptance | 144 | 0 | 139 | -96.5 | 2.87e-42 |
| qwen3.5-4b-ft-multi | none | Silent wrong recommendation | 144 | 0 | 121 | -84.0 | 7.523e-37 |
| qwen3.5-4b-ft-multi | informative | Planted acceptance | 144 | 0 | 134 | -93.1 | 9.184e-41 |
| qwen3.5-4b-ft-multi | informative | Silent wrong recommendation | 144 | 0 | 114 | -79.2 | 9.63e-35 |
| qwen3.5-4b-ft-multi | placebo | Planted acceptance | 144 | 0 | 133 | -92.4 | 1.837e-40 |
| qwen3.5-4b-ft-multi | placebo | Silent wrong recommendation | 144 | 0 | 120 | -83.3 | 1.505e-36 |
| qwen3.5-4b-ft-multi | forged | Planted acceptance | 144 | 0 | 135 | -93.8 | 4.592e-41 |
| qwen3.5-4b-ft-multi | forged | Silent wrong recommendation | 144 | 0 | 79 | -54.9 | 3.309e-24 |

## English-trained arm transfer

For each target language, both arms and both languages must have a valid verdict for the same fact.
The transfer contrast is the fine-tune minus base change in the target language minus that change in English.
A negative contrast for planted acceptance or silent wrong recommendation means a larger reduction in the target language.

| Label | Truth | Target language | Outcome | Matched facts | Change in English (pp) | Change in target (pp) | Transfer contrast (pp) |
|---|---|---|---|---:|---:|---:|---:|
| none | real | hi | Real-update acceptance | 48 | -95.8 | -31.2 | +64.6 |
| none | real | hi | Deferral | 48 | +95.8 | +29.2 | -66.7 |
| none | real | hi | Disclosure | 48 | +89.6 | +68.8 | -20.8 |
| none | real | hinglish | Real-update acceptance | 48 | -95.8 | -25.0 | +70.8 |
| none | real | hinglish | Deferral | 48 | +95.8 | +16.7 | -79.2 |
| none | real | hinglish | Disclosure | 48 | +89.6 | +89.6 | +0.0 |
| none | planted | hi | Planted-claim acceptance | 48 | -95.8 | -31.2 | +64.6 |
| none | planted | hi | Deferral | 48 | +95.8 | +25.0 | -70.8 |
| none | planted | hi | Disclosure | 48 | +91.7 | +70.8 | -20.8 |
| none | planted | hi | Silent wrong recommendation | 48 | -91.7 | -70.8 | +20.8 |
| none | planted | hinglish | Planted-claim acceptance | 48 | -95.8 | -27.1 | +68.8 |
| none | planted | hinglish | Deferral | 48 | +95.8 | +18.8 | -77.1 |
| none | planted | hinglish | Disclosure | 48 | +91.7 | +89.6 | -2.1 |
| none | planted | hinglish | Silent wrong recommendation | 48 | -91.7 | -87.5 | +4.2 |
| informative | real | hi | Real-update acceptance | 48 | -45.8 | -6.2 | +39.6 |
| informative | real | hi | Deferral | 48 | +45.8 | -4.2 | -50.0 |
| informative | real | hi | Disclosure | 48 | +89.6 | +70.8 | -18.8 |
| informative | real | hinglish | Real-update acceptance | 48 | -45.8 | -18.8 | +27.1 |
| informative | real | hinglish | Deferral | 48 | +45.8 | +6.2 | -39.6 |
| informative | real | hinglish | Disclosure | 48 | +89.6 | +89.6 | +0.0 |
| informative | planted | hi | Planted-claim acceptance | 48 | -100.0 | -50.0 | +50.0 |
| informative | planted | hi | Deferral | 48 | +25.0 | +10.4 | -14.6 |
| informative | planted | hi | Disclosure | 48 | +83.3 | +70.8 | -12.5 |
| informative | planted | hi | Silent wrong recommendation | 48 | -83.3 | -68.8 | +14.6 |
| informative | planted | hinglish | Planted-claim acceptance | 48 | -100.0 | -91.7 | +8.3 |
| informative | planted | hinglish | Deferral | 48 | +25.0 | +2.1 | -22.9 |
| informative | planted | hinglish | Disclosure | 48 | +83.3 | +83.3 | +0.0 |
| informative | planted | hinglish | Silent wrong recommendation | 48 | -83.3 | -79.2 | +4.2 |
| placebo | real | hi | Real-update acceptance | 48 | -89.6 | -22.9 | +66.7 |
| placebo | real | hi | Deferral | 48 | +91.7 | +10.4 | -81.2 |
| placebo | real | hi | Disclosure | 48 | +83.3 | +77.1 | -6.2 |
| placebo | real | hinglish | Real-update acceptance | 48 | -89.6 | -52.1 | +37.5 |
| placebo | real | hinglish | Deferral | 48 | +91.7 | +18.8 | -72.9 |
| placebo | real | hinglish | Disclosure | 48 | +83.3 | +85.4 | +2.1 |
| placebo | planted | hi | Planted-claim acceptance | 48 | -89.6 | -22.9 | +66.7 |
| placebo | planted | hi | Deferral | 48 | +91.7 | +12.5 | -79.2 |
| placebo | planted | hi | Disclosure | 48 | +83.3 | +72.9 | -10.4 |
| placebo | planted | hi | Silent wrong recommendation | 48 | -83.3 | -72.9 | +10.4 |
| placebo | planted | hinglish | Planted-claim acceptance | 48 | -89.6 | -52.1 | +37.5 |
| placebo | planted | hinglish | Deferral | 48 | +91.7 | +16.7 | -75.0 |
| placebo | planted | hinglish | Disclosure | 48 | +83.3 | +85.4 | +2.1 |
| placebo | planted | hinglish | Silent wrong recommendation | 48 | -83.3 | -83.3 | +0.0 |
| forged | real | hi | Real-update acceptance | 48 | -20.8 | -6.2 | +14.6 |
| forged | real | hi | Deferral | 48 | +16.7 | +4.2 | -12.5 |
| forged | real | hi | Disclosure | 48 | +70.8 | +54.2 | -16.7 |
| forged | real | hinglish | Real-update acceptance | 48 | -20.8 | -12.5 | +8.3 |
| forged | real | hinglish | Deferral | 48 | +16.7 | +2.1 | -14.6 |
| forged | real | hinglish | Disclosure | 48 | +70.8 | +66.7 | -4.2 |
| forged | planted | hi | Planted-claim acceptance | 48 | -95.8 | -50.0 | +45.8 |
| forged | planted | hi | Deferral | 48 | +10.4 | +4.2 | -6.2 |
| forged | planted | hi | Disclosure | 48 | +60.4 | +43.8 | -16.7 |
| forged | planted | hi | Silent wrong recommendation | 48 | -60.4 | -41.7 | +18.7 |
| forged | planted | hinglish | Planted-claim acceptance | 48 | -95.8 | -87.5 | +8.3 |
| forged | planted | hinglish | Deferral | 48 | +10.4 | +6.2 | -4.2 |
| forged | planted | hinglish | Disclosure | 48 | +60.4 | +60.4 | +0.0 |
| forged | planted | hinglish | Silent wrong recommendation | 48 | -60.4 | -60.4 | +0.0 |
