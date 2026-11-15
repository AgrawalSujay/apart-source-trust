Partial snapshot | exploratory fine-tune plan: 3,456 rows (qwen3.5-4b-base, qwen3.5-4b-ft-en, qwen3.5-4b-ft-multi)
Observed 3,456 rows (qwen3.5-4b-base, qwen3.5-4b-ft-en, qwen3.5-4b-ft-multi); analysed 3,456, 0 unresolved, 0 duplicate rows.

# Results

| Hypothesis | Estimate | p | p (Holm) | Supported |
|---|---|---|---|---|
| H1 | 47.3% adopt (n=864) | 0.945 | 1 | no |
| H2 | DiD 35.6 pts, 95% CI [30.8, 40.7] | 0 | 0 | yes |
| H3 | 15 vs 6 discordant pairs (of 432) | 0.0392 | 0.274 | no |
| H4 | 21 vs 26 discordant pairs (of 432) | 0.56 | 1 | no |
| H5_hi | 20 vs 5 discordant pairs (of 144) | 0.00204 | 0.0163 | yes |
| H5_hinglish | 0 vs 4 discordant pairs (of 144) | 1 | 1 | no |
| H6 | 50.0% disclose (n=1809) | 0.5 | 1 | no |
| H7_hi | 13 vs 21 discordant pairs (of 288) | 0.939 | 1 | no |
| H7_hinglish | 9 vs 10 discordant pairs (of 288) | 0.676 | 1 | no |

## Pre-registered outcome

| Model | Label | Real accepted | Planted accepted | Discrimination | Silent error | Correct source | Disclosure (adopters) | Neither |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-4b-base | none | 96.5 | 96.5 | 0.0 | 83.3 | 49.3 | 14.4 | 0.7 |
| qwen3.5-4b-base | informative | 94.4 | 93.8 | 0.7 | 79.2 | 49.7 | 13.3 | 0.3 |
| qwen3.5-4b-base | placebo | 95.1 | 95.1 | 0.0 | 83.3 | 49.3 | 12.4 | 0.0 |
| qwen3.5-4b-base | forged | 97.9 | 95.1 | 2.8 | 54.9 | 51.0 | 38.8 | 0.0 |
| qwen3.5-4b-ft-en | none | 45.8 | 45.1 | 0.7 | 0.7 | 26.7 | 98.5 | 0.7 |
| qwen3.5-4b-ft-en | informative | 70.8 | 13.2 | 57.6 | 2.1 | 72.6 | 92.6 | 0.3 |
| qwen3.5-4b-ft-en | placebo | 40.3 | 40.3 | 0.0 | 3.5 | 29.2 | 92.2 | 0.7 |
| qwen3.5-4b-ft-en | forged | 84.7 | 17.4 | 67.4 | 0.7 | 80.6 | 98.6 | 0.0 |
| qwen3.5-4b-ft-multi | none | 0.0 | 0.0 | 0.0 | 0.0 | 0.7 | – | 0.0 |
| qwen3.5-4b-ft-multi | informative | 50.0 | 0.7 | 49.3 | 0.0 | 66.7 | 100.0 | 0.0 |
| qwen3.5-4b-ft-multi | placebo | 2.8 | 2.8 | 0.0 | 0.0 | 2.1 | 100.0 | 0.0 |
| qwen3.5-4b-ft-multi | forged | 76.4 | 1.4 | 75.0 | 0.0 | 83.0 | 100.0 | 0.0 |
| pooled | none | 47.5 | 47.2 | 0.2 | 28.0 | 25.6 | 41.3 | 0.5 |
| pooled | informative | 71.8 | 35.9 | 35.9 | 27.1 | 63.0 | 47.5 | 0.2 |
| pooled | placebo | 46.1 | 46.1 | 0.0 | 28.9 | 26.9 | 37.4 | 0.2 |
| pooled | forged | 86.3 | 38.0 | 48.4 | 18.5 | 71.5 | 68.0 | 0.0 |

Pooled by language (%)

| Label | Language | Planted accepted | Silent error | Relay absent | Fact | Hedged | Attributed |
|---|---|---|---|---|---|---|---|
| none | en | 34.7 | 30.6 | 0.0 | 31.9 | 47.6 | 20.5 |
| none | hi | 50.7 | 24.3 | 2.1 | 31.9 | 5.6 | 60.4 |
| none | hinglish | 56.2 | 29.2 | 0.0 | 36.1 | 17.7 | 46.2 |
| informative | en | 33.3 | 27.8 | 0.0 | 27.1 | 5.9 | 67.0 |
| informative | hi | 43.8 | 27.1 | 4.9 | 26.0 | 3.5 | 65.6 |
| informative | hinglish | 30.6 | 26.4 | 1.4 | 31.6 | 1.0 | 66.0 |
| placebo | en | 36.1 | 29.2 | 0.0 | 30.6 | 50.7 | 18.8 |
| placebo | hi | 55.6 | 29.9 | 3.1 | 33.3 | 5.2 | 58.3 |
| placebo | hinglish | 46.5 | 27.8 | 2.1 | 33.7 | 4.2 | 60.1 |
| forged | en | 35.4 | 20.1 | 0.0 | 14.6 | 1.0 | 84.4 |
| forged | hi | 43.8 | 15.3 | 1.7 | 7.3 | 3.1 | 87.8 |
| forged | hinglish | 34.7 | 20.1 | 1.0 | 13.2 | 4.2 | 81.6 |

## Recommendation view (deviation 4)

| Model | Label | Real accepted | Planted accepted | Discrimination | Silent error | Correct source | Disclosure (adopters) | Neither |
|---|---|---|---|---|---|---|---|---|
| qwen3.5-4b-base | none | 97.2 | 97.2 | 0.0 | 84.0 | 49.7 | 14.3 | 0.0 |
| qwen3.5-4b-base | informative | 93.8 | 93.1 | 0.7 | 79.2 | 49.3 | 12.6 | 1.0 |
| qwen3.5-4b-base | placebo | 95.1 | 95.1 | 0.0 | 83.3 | 49.3 | 12.4 | 0.3 |
| qwen3.5-4b-base | forged | 97.9 | 95.1 | 2.8 | 54.9 | 51.0 | 38.8 | 0.0 |
| qwen3.5-4b-ft-en | none | 45.8 | 45.1 | 0.7 | 0.7 | 26.7 | 98.5 | 46.9 |
| qwen3.5-4b-ft-en | informative | 70.8 | 11.1 | 59.7 | 2.1 | 72.6 | 92.4 | 16.7 |
| qwen3.5-4b-ft-en | placebo | 40.3 | 40.3 | 0.0 | 3.5 | 29.2 | 92.2 | 41.0 |
| qwen3.5-4b-ft-en | forged | 84.7 | 16.0 | 68.8 | 0.7 | 80.6 | 98.6 | 7.3 |
| qwen3.5-4b-ft-multi | none | 0.0 | 0.0 | 0.0 | 0.0 | 0.7 | – | 98.6 |
| qwen3.5-4b-ft-multi | informative | 50.0 | 0.7 | 49.3 | 0.0 | 66.7 | 100.0 | 31.9 |
| qwen3.5-4b-ft-multi | placebo | 2.8 | 2.8 | 0.0 | 0.0 | 2.1 | 100.0 | 95.8 |
| qwen3.5-4b-ft-multi | forged | 76.4 | 1.4 | 75.0 | 0.0 | 83.0 | 100.0 | 15.6 |
| pooled | none | 47.7 | 47.5 | 0.2 | 28.2 | 25.7 | 41.1 | 48.5 |
| pooled | informative | 71.5 | 35.0 | 36.6 | 27.1 | 62.8 | 47.0 | 16.6 |
| pooled | placebo | 46.1 | 46.1 | 0.0 | 28.9 | 26.9 | 37.4 | 45.7 |
| pooled | forged | 86.3 | 37.5 | 48.8 | 18.5 | 71.5 | 67.9 | 7.6 |

Pooled by language (%)

| Label | Language | Planted accepted | Silent error | Relay absent | Fact | Hedged | Attributed |
|---|---|---|---|---|---|---|---|
| none | en | 34.7 | 30.6 | 0.0 | 31.9 | 47.6 | 20.5 |
| none | hi | 51.4 | 25.0 | 2.1 | 31.9 | 5.6 | 60.4 |
| none | hinglish | 56.2 | 29.2 | 0.0 | 36.1 | 17.7 | 46.2 |
| informative | en | 33.3 | 27.8 | 0.0 | 27.1 | 5.9 | 67.0 |
| informative | hi | 41.0 | 27.1 | 4.9 | 26.0 | 3.5 | 65.6 |
| informative | hinglish | 30.6 | 26.4 | 1.4 | 31.6 | 1.0 | 66.0 |
| placebo | en | 36.1 | 29.2 | 0.0 | 30.6 | 50.7 | 18.8 |
| placebo | hi | 55.6 | 29.9 | 3.1 | 33.3 | 5.2 | 58.3 |
| placebo | hinglish | 46.5 | 27.8 | 2.1 | 33.7 | 4.2 | 60.1 |
| forged | en | 35.4 | 20.1 | 0.0 | 14.6 | 1.0 | 84.4 |
| forged | hi | 43.1 | 15.3 | 1.7 | 7.3 | 3.1 | 87.8 |
| forged | hinglish | 34.0 | 20.1 | 1.0 | 13.2 | 4.2 | 81.6 |
