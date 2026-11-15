Partial snapshot | confirmatory plan: 8,064 rows (deepseek-v4.1-flash-1017, glm-5.3, qwen3.8-27b, gemma-4-31b-it, gemma-4-26b-a4b-it, qwen3.5-397b, glm-5.2)
Observed 8,064 rows (deepseek-v4.1-flash-1017, gemma-4-26b-a4b-it, gemma-4-31b-it, glm-5.2, glm-5.3, qwen3.5-397b, qwen3.8-27b); analysed 8,064, 0 unresolved, 0 duplicate rows.

# Results

| Hypothesis | Estimate | p | p (Holm) | Supported |
|---|---|---|---|---|
| H1 | 27.4% adopt (n=2016) | 1 | 1 | no |
| H2 | DiD 90.8 pts, 95% CI [89.0, 92.5] | 0 | 0 | yes |
| H3 | 193 vs 3 discordant pairs (of 1008) | 1.25e-53 | 1e-52 | yes |
| H4 | 66 vs 83 discordant pairs (of 1008) | 0.19 | 0.569 | no |
| H5_hi | 22 vs 0 discordant pairs (of 336) | 2.38e-07 | 1.67e-06 | yes |
| H5_hinglish | 14 vs 2 discordant pairs (of 336) | 0.00209 | 0.00836 | yes |
| H6 | 76.3% disclose (n=3291) | 1 | 1 | no |
| H7_hi | 72 vs 34 discordant pairs (of 672) | 0.000142 | 0.000711 | yes |
| H7_hinglish | 64 vs 24 discordant pairs (of 672) | 1.19e-05 | 7.12e-05 | yes |

## Pre-registered outcome

| Model | Label | Real accepted | Planted accepted | Discrimination | Silent error | Correct source | Disclosure (adopters) | Neither |
|---|---|---|---|---|---|---|---|---|
| deepseek-v4.1-flash-1017 | none | 20.8 | 20.8 | 0.0 | 0.7 | 25.7 | 96.7 | 0.0 |
| deepseek-v4.1-flash-1017 | informative | 97.2 | 0.7 | 96.5 | 0.0 | 91.7 | 99.3 | 0.0 |
| deepseek-v4.1-flash-1017 | placebo | 18.1 | 17.4 | 0.7 | 0.0 | 20.5 | 100.0 | 0.0 |
| deepseek-v4.1-flash-1017 | forged | 97.9 | 12.5 | 85.4 | 0.0 | 86.1 | 100.0 | 0.0 |
| gemma-4-26b-a4b-it | none | 61.8 | 61.8 | 0.0 | 20.8 | 31.9 | 66.3 | 0.0 |
| gemma-4-26b-a4b-it | informative | 91.7 | 25.0 | 66.7 | 10.4 | 61.5 | 67.3 | 0.0 |
| gemma-4-26b-a4b-it | placebo | 64.6 | 64.6 | 0.0 | 24.3 | 33.3 | 62.4 | 0.0 |
| gemma-4-26b-a4b-it | forged | 100.0 | 86.1 | 13.9 | 27.1 | 54.5 | 66.0 | 0.0 |
| gemma-4-31b-it | none | 78.5 | 78.5 | 0.0 | 45.1 | 41.0 | 42.5 | 3.5 |
| gemma-4-31b-it | informative | 95.1 | 0.0 | 95.1 | 0.0 | 95.8 | 59.1 | 3.5 |
| gemma-4-31b-it | placebo | 64.6 | 64.6 | 0.0 | 36.8 | 37.5 | 43.0 | 2.1 |
| gemma-4-31b-it | forged | 97.2 | 33.3 | 63.9 | 20.1 | 80.6 | 53.2 | 2.8 |
| glm-5.2 | none | 1.4 | 1.4 | 0.0 | 0.0 | 3.5 | 100.0 | 0.7 |
| glm-5.2 | informative | 95.8 | 0.0 | 95.8 | 0.0 | 97.6 | 99.3 | 0.0 |
| glm-5.2 | placebo | 0.0 | 0.0 | 0.0 | 0.0 | 3.5 | – | 0.0 |
| glm-5.2 | forged | 95.8 | 0.0 | 95.8 | 0.0 | 97.6 | 99.3 | 0.3 |
| glm-5.3 | none | 0.0 | 0.0 | 0.0 | 0.0 | 2.4 | – | 0.0 |
| glm-5.3 | informative | 99.3 | 0.0 | 99.3 | 0.0 | 99.7 | 100.0 | 0.0 |
| glm-5.3 | placebo | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | – | 0.0 |
| glm-5.3 | forged | 100.0 | 0.0 | 100.0 | 0.0 | 99.7 | 100.0 | 0.3 |
| qwen3.5-397b | none | 3.5 | 3.5 | 0.0 | 0.0 | 4.9 | 100.0 | 0.0 |
| qwen3.5-397b | informative | 97.9 | 0.0 | 97.9 | 0.0 | 98.6 | 100.0 | 0.0 |
| qwen3.5-397b | placebo | 12.5 | 12.5 | 0.0 | 2.8 | 8.7 | 77.8 | 0.3 |
| qwen3.5-397b | forged | 99.3 | 2.8 | 96.5 | 0.0 | 96.2 | 99.3 | 0.0 |
| qwen3.8-27b | none | 25.7 | 25.7 | 0.0 | 13.9 | 17.7 | 45.9 | 9.0 |
| qwen3.8-27b | informative | 88.2 | 4.2 | 84.0 | 2.8 | 78.5 | 82.0 | 3.1 |
| qwen3.8-27b | placebo | 20.8 | 20.8 | 0.0 | 6.9 | 15.6 | 66.7 | 2.8 |
| qwen3.8-27b | forged | 94.4 | 27.1 | 67.4 | 6.9 | 75.7 | 85.1 | 4.5 |
| pooled | none | 27.4 | 27.4 | 0.0 | 11.5 | 18.2 | 58.0 | 1.9 |
| pooled | informative | 95.0 | 4.3 | 90.8 | 1.9 | 89.0 | 86.3 | 0.9 |
| pooled | placebo | 25.8 | 25.7 | 0.1 | 10.1 | 17.2 | 60.7 | 0.7 |
| pooled | forged | 97.8 | 23.1 | 74.7 | 7.7 | 84.3 | 83.0 | 1.1 |

Pooled by language (%)

| Label | Language | Planted accepted | Silent error | Relay absent | Fact | Hedged | Attributed |
|---|---|---|---|---|---|---|---|
| none | en | 15.5 | 8.9 | 1.2 | 11.0 | 39.4 | 48.4 |
| none | hi | 30.7 | 11.6 | 3.9 | 12.8 | 22.5 | 60.9 |
| none | hinglish | 36.0 | 14.0 | 1.8 | 16.1 | 22.0 | 60.1 |
| informative | en | 0.9 | 0.9 | 7.0 | 9.2 | 0.3 | 83.5 |
| informative | hi | 7.4 | 2.7 | 3.0 | 5.4 | 1.0 | 90.6 |
| informative | hinglish | 4.5 | 2.1 | 3.1 | 10.1 | 0.4 | 86.3 |
| placebo | en | 11.0 | 7.4 | 2.4 | 8.3 | 10.1 | 79.2 |
| placebo | hi | 29.5 | 7.1 | 1.2 | 8.0 | 12.6 | 78.1 |
| placebo | hinglish | 36.6 | 15.8 | 1.3 | 18.5 | 11.3 | 68.9 |
| forged | en | 9.8 | 5.4 | 6.0 | 13.7 | 0.6 | 79.8 |
| forged | hi | 31.2 | 6.2 | 2.5 | 9.4 | 0.9 | 87.2 |
| forged | hinglish | 28.3 | 11.6 | 3.0 | 15.0 | 0.9 | 81.1 |

## Recommendation view (deviation 4)

| Model | Label | Real accepted | Planted accepted | Discrimination | Silent error | Correct source | Disclosure (adopters) | Neither |
|---|---|---|---|---|---|---|---|---|
| deepseek-v4.1-flash-1017 | none | 20.8 | 20.8 | 0.0 | 0.7 | 25.7 | 96.7 | 48.6 |
| deepseek-v4.1-flash-1017 | informative | 97.2 | 0.7 | 96.5 | 0.0 | 91.7 | 99.3 | 7.6 |
| deepseek-v4.1-flash-1017 | placebo | 18.1 | 17.4 | 0.7 | 0.0 | 20.5 | 100.0 | 59.4 |
| deepseek-v4.1-flash-1017 | forged | 97.9 | 12.5 | 85.4 | 0.0 | 86.1 | 100.0 | 7.6 |
| gemma-4-26b-a4b-it | none | 61.8 | 61.8 | 0.0 | 20.8 | 31.9 | 66.3 | 36.1 |
| gemma-4-26b-a4b-it | informative | 91.7 | 25.0 | 66.7 | 10.4 | 60.8 | 67.3 | 26.4 |
| gemma-4-26b-a4b-it | placebo | 64.6 | 64.6 | 0.0 | 24.3 | 33.3 | 62.4 | 33.3 |
| gemma-4-26b-a4b-it | forged | 100.0 | 86.1 | 13.9 | 27.1 | 54.5 | 66.0 | 2.4 |
| gemma-4-31b-it | none | 78.5 | 78.5 | 0.0 | 45.1 | 41.0 | 42.5 | 17.4 |
| gemma-4-31b-it | informative | 95.1 | 0.0 | 95.1 | 0.0 | 95.8 | 59.1 | 3.8 |
| gemma-4-31b-it | placebo | 64.6 | 64.6 | 0.0 | 36.8 | 37.2 | 43.0 | 25.7 |
| gemma-4-31b-it | forged | 97.2 | 33.3 | 63.9 | 20.1 | 80.6 | 53.2 | 2.8 |
| glm-5.2 | none | 1.4 | 1.4 | 0.0 | 0.0 | 3.5 | 100.0 | 92.4 |
| glm-5.2 | informative | 95.8 | 0.0 | 95.8 | 0.0 | 97.6 | 99.3 | 0.3 |
| glm-5.2 | placebo | 0.0 | 0.0 | 0.0 | 0.0 | 3.5 | – | 93.1 |
| glm-5.2 | forged | 95.8 | 0.0 | 95.8 | 0.0 | 97.6 | 99.3 | 0.7 |
| glm-5.3 | none | 0.0 | 0.0 | 0.0 | 0.0 | 2.4 | – | 95.1 |
| glm-5.3 | informative | 99.3 | 0.0 | 99.3 | 0.0 | 99.7 | 100.0 | 0.0 |
| glm-5.3 | placebo | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | – | 97.9 |
| glm-5.3 | forged | 100.0 | 0.0 | 100.0 | 0.0 | 99.7 | 100.0 | 0.3 |
| qwen3.5-397b | none | 3.5 | 3.5 | 0.0 | 0.0 | 4.9 | 100.0 | 90.3 |
| qwen3.5-397b | informative | 97.9 | 0.0 | 97.9 | 0.0 | 98.6 | 100.0 | 0.3 |
| qwen3.5-397b | placebo | 12.5 | 12.5 | 0.0 | 2.8 | 8.7 | 77.8 | 82.6 |
| qwen3.5-397b | forged | 99.3 | 2.8 | 96.5 | 0.0 | 96.2 | 99.3 | 2.1 |
| qwen3.8-27b | none | 25.7 | 25.7 | 0.0 | 13.9 | 17.4 | 45.9 | 65.3 |
| qwen3.8-27b | informative | 88.2 | 4.2 | 84.0 | 2.8 | 76.7 | 82.0 | 19.8 |
| qwen3.8-27b | placebo | 20.8 | 20.8 | 0.0 | 6.9 | 15.6 | 66.7 | 68.8 |
| qwen3.8-27b | forged | 94.4 | 27.1 | 67.4 | 6.9 | 75.3 | 85.1 | 10.4 |
| pooled | none | 27.4 | 27.4 | 0.0 | 11.5 | 18.1 | 58.0 | 63.6 |
| pooled | informative | 95.0 | 4.3 | 90.8 | 1.9 | 88.7 | 86.3 | 8.3 |
| pooled | placebo | 25.8 | 25.7 | 0.1 | 10.1 | 17.1 | 60.7 | 65.8 |
| pooled | forged | 97.8 | 23.1 | 74.7 | 7.7 | 84.3 | 83.0 | 3.8 |

Pooled by language (%)

| Label | Language | Planted accepted | Silent error | Relay absent | Fact | Hedged | Attributed |
|---|---|---|---|---|---|---|---|
| none | en | 15.5 | 8.9 | 1.2 | 11.0 | 39.4 | 48.4 |
| none | hi | 30.7 | 11.6 | 3.9 | 12.8 | 22.5 | 60.9 |
| none | hinglish | 36.0 | 14.0 | 1.8 | 16.1 | 22.0 | 60.1 |
| informative | en | 0.9 | 0.9 | 7.0 | 9.2 | 0.3 | 83.5 |
| informative | hi | 7.4 | 2.7 | 3.0 | 5.4 | 1.0 | 90.6 |
| informative | hinglish | 4.5 | 2.1 | 3.1 | 10.1 | 0.4 | 86.3 |
| placebo | en | 11.0 | 7.4 | 2.4 | 8.3 | 10.1 | 79.2 |
| placebo | hi | 29.5 | 7.1 | 1.2 | 8.0 | 12.6 | 78.1 |
| placebo | hinglish | 36.6 | 15.8 | 1.3 | 18.5 | 11.3 | 68.9 |
| forged | en | 9.8 | 5.4 | 6.0 | 13.7 | 0.6 | 79.8 |
| forged | hi | 31.2 | 6.2 | 2.5 | 9.4 | 0.9 | 87.2 |
| forged | hinglish | 28.3 | 11.6 | 3.0 | 15.0 | 0.9 | 81.1 |
