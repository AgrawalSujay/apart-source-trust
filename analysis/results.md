# Results

| Hypothesis | Estimate | p | p (Holm) | Supported |
|---|---|---|---|---|
| H1 | 97.8% adopt (n=2016) | 0 | 0 | yes |
| H2 | DiD 51.2 pts, 95% CI [46.5, 55.9] | 0 | 0 | yes |
| H3 | 234 vs 12 discordant pairs (of 1008) | 7.27e-55 | 4.36e-54 | yes |
| H4 | 13 vs 13 discordant pairs (of 1008) | 1 | 1 | no |
| H5_hi | 69 vs 8 discordant pairs (of 336) | 1.57e-13 | 4.71e-13 | yes |
| H5_hinglish | 73 vs 8 discordant pairs (of 336) | 1.49e-14 | 5.95e-14 | yes |
| H6 | 22.2% disclose (n=7088) | 0 | 0 | yes |
| H7_hi | 71 vs 42 discordant pairs (of 672) | 0.00407 | 0.00815 | yes |
| H7_hinglish | 127 vs 20 discordant pairs (of 672) | 1.56e-20 | 7.81e-20 | yes |

## Pre-registered outcome

| Model | Label | Real accepted | Planted accepted | Discrimination | Silent error | Correct source | Disclosure (adopters) | Neither |
|---|---|---|---|---|---|---|---|---|
| deepseek-v4.1-flash-1017 | none | 100.0 | 100.0 | 0.0 | 62.5 | 50.0 | 36.8 | 0.0 |
| deepseek-v4.1-flash-1017 | informative | 99.3 | 42.4 | 56.9 | 16.7 | 64.6 | 55.9 | 0.7 |
| deepseek-v4.1-flash-1017 | placebo | 98.6 | 99.3 | -0.7 | 49.3 | 49.3 | 49.5 | 0.0 |
| deepseek-v4.1-flash-1017 | forged | 100.0 | 69.4 | 30.6 | 27.1 | 57.6 | 58.2 | 1.0 |
| gemma-4-26b-a4b-it | none | 100.0 | 100.0 | 0.0 | 98.6 | 50.0 | 1.4 | 0.0 |
| gemma-4-26b-a4b-it | informative | 100.0 | 97.2 | 2.8 | 93.8 | 50.7 | 3.2 | 0.0 |
| gemma-4-26b-a4b-it | placebo | 99.3 | 99.3 | 0.0 | 98.6 | 49.7 | 0.7 | 0.7 |
| gemma-4-26b-a4b-it | forged | 100.0 | 100.0 | 0.0 | 90.3 | 50.0 | 7.3 | 0.0 |
| gemma-4-31b-it | none | 98.6 | 98.6 | 0.0 | 97.9 | 49.3 | 0.7 | 1.4 |
| gemma-4-31b-it | informative | 98.6 | 79.2 | 19.4 | 79.2 | 59.7 | 0.0 | 0.7 |
| gemma-4-31b-it | placebo | 99.3 | 99.3 | 0.0 | 99.3 | 49.7 | 0.0 | 0.7 |
| gemma-4-31b-it | forged | 99.3 | 99.3 | 0.0 | 97.2 | 49.7 | 1.4 | 0.7 |
| glm-5.2 | none | 88.9 | 88.9 | 0.0 | 71.5 | 47.6 | 19.5 | 0.0 |
| glm-5.2 | informative | 95.8 | 10.4 | 85.4 | 4.9 | 87.5 | 43.1 | 0.0 |
| glm-5.2 | placebo | 91.7 | 91.7 | 0.0 | 66.0 | 47.6 | 28.4 | 0.7 |
| glm-5.2 | forged | 98.6 | 36.1 | 62.5 | 16.7 | 69.1 | 39.2 | 0.0 |
| glm-5.3 | none | 100.0 | 100.0 | 0.0 | 43.1 | 50.0 | 57.3 | 0.0 |
| glm-5.3 | informative | 100.0 | 1.4 | 98.6 | 0.7 | 90.3 | 70.5 | 0.0 |
| glm-5.3 | placebo | 98.6 | 100.0 | -1.4 | 34.7 | 49.3 | 67.1 | 0.0 |
| glm-5.3 | forged | 99.3 | 10.4 | 88.9 | 2.1 | 78.1 | 68.4 | 0.0 |
| qwen3.5-397b | none | 100.0 | 100.0 | 0.0 | 95.1 | 50.0 | 4.9 | 0.0 |
| qwen3.5-397b | informative | 100.0 | 45.1 | 54.9 | 40.3 | 76.4 | 8.1 | 0.0 |
| qwen3.5-397b | placebo | 100.0 | 100.0 | 0.0 | 93.1 | 50.0 | 6.9 | 0.0 |
| qwen3.5-397b | forged | 98.6 | 93.8 | 4.9 | 79.2 | 52.4 | 14.8 | 0.7 |
| qwen3.8-27b | none | 97.2 | 97.2 | 0.0 | 90.3 | 48.6 | 7.1 | 2.8 |
| qwen3.8-27b | informative | 91.7 | 51.4 | 40.3 | 43.8 | 53.5 | 11.7 | 17.4 |
| qwen3.8-27b | placebo | 94.4 | 95.1 | -0.7 | 88.9 | 47.2 | 7.3 | 4.9 |
| qwen3.8-27b | forged | 96.5 | 72.2 | 24.3 | 60.4 | 52.1 | 15.6 | 10.8 |
| pooled | none | 97.8 | 97.8 | 0.0 | 79.9 | 49.4 | 18.3 | 0.6 |
| pooled | informative | 97.9 | 46.7 | 51.2 | 39.9 | 68.9 | 22.8 | 2.7 |
| pooled | placebo | 97.4 | 97.8 | -0.4 | 75.7 | 49.0 | 22.9 | 1.0 |
| pooled | forged | 98.9 | 68.8 | 30.2 | 53.3 | 58.4 | 25.4 | 1.9 |

Pooled by language (%)

| Label | Language | Planted accepted | Silent error | Relay absent | Fact | Hedged | Attributed |
|---|---|---|---|---|---|---|---|
| none | en | 97.6 | 73.2 | 1.2 | 78.1 | 5.7 | 15.0 |
| none | hi | 97.9 | 77.4 | 1.5 | 80.8 | 3.7 | 14.0 |
| none | hinglish | 97.9 | 89.0 | 1.5 | 89.6 | 1.8 | 7.1 |
| informative | en | 34.2 | 27.7 | 12.6 | 43.5 | 0.4 | 43.5 |
| informative | hi | 52.4 | 42.9 | 8.5 | 50.7 | 1.9 | 38.8 |
| informative | hinglish | 53.6 | 49.1 | 10.3 | 62.8 | 0.6 | 26.3 |
| placebo | en | 97.3 | 65.8 | 1.9 | 69.2 | 6.1 | 22.8 |
| placebo | hi | 98.2 | 73.2 | 1.2 | 74.0 | 3.0 | 21.9 |
| placebo | hinglish | 97.9 | 88.1 | 1.5 | 87.9 | 1.2 | 9.4 |
| forged | en | 59.2 | 43.8 | 4.3 | 45.8 | 0.6 | 49.3 |
| forged | hi | 71.1 | 51.2 | 3.3 | 43.6 | 0.4 | 52.7 |
| forged | hinglish | 75.9 | 64.9 | 1.6 | 61.6 | 0.4 | 36.3 |

## Recommendation view (deviation 4)

| Model | Label | Real accepted | Planted accepted | Discrimination | Silent error | Correct source | Disclosure (adopters) | Neither |
|---|---|---|---|---|---|---|---|---|
| deepseek-v4.1-flash-1017 | none | 100.0 | 100.0 | 0.0 | 62.5 | 50.0 | 36.8 | 0.0 |
| deepseek-v4.1-flash-1017 | informative | 99.3 | 42.4 | 56.9 | 16.7 | 64.2 | 55.9 | 14.6 |
| deepseek-v4.1-flash-1017 | placebo | 98.6 | 99.3 | -0.7 | 49.3 | 49.3 | 49.5 | 0.7 |
| deepseek-v4.1-flash-1017 | forged | 100.0 | 69.4 | 30.6 | 27.1 | 57.6 | 58.2 | 7.6 |
| gemma-4-26b-a4b-it | none | 100.0 | 100.0 | 0.0 | 98.6 | 50.0 | 1.4 | 0.0 |
| gemma-4-26b-a4b-it | informative | 100.0 | 97.2 | 2.8 | 93.8 | 50.7 | 3.2 | 0.7 |
| gemma-4-26b-a4b-it | placebo | 99.3 | 99.3 | 0.0 | 98.6 | 49.7 | 0.7 | 0.7 |
| gemma-4-26b-a4b-it | forged | 100.0 | 100.0 | 0.0 | 90.3 | 50.0 | 7.3 | 0.0 |
| gemma-4-31b-it | none | 98.6 | 98.6 | 0.0 | 97.9 | 49.3 | 0.7 | 1.4 |
| gemma-4-31b-it | informative | 98.6 | 79.2 | 19.4 | 79.2 | 59.7 | 0.0 | 0.7 |
| gemma-4-31b-it | placebo | 99.3 | 99.3 | 0.0 | 99.3 | 49.7 | 0.0 | 0.7 |
| gemma-4-31b-it | forged | 99.3 | 99.3 | 0.0 | 97.2 | 49.7 | 1.4 | 0.7 |
| glm-5.2 | none | 88.9 | 88.9 | 0.0 | 71.5 | 47.6 | 19.5 | 4.9 |
| glm-5.2 | informative | 95.8 | 10.4 | 85.4 | 4.9 | 87.5 | 43.1 | 6.6 |
| glm-5.2 | placebo | 91.7 | 91.7 | 0.0 | 66.0 | 47.6 | 28.4 | 4.9 |
| glm-5.2 | forged | 98.6 | 36.1 | 62.5 | 16.7 | 69.1 | 39.2 | 12.8 |
| glm-5.3 | none | 100.0 | 100.0 | 0.0 | 43.1 | 50.0 | 57.3 | 0.0 |
| glm-5.3 | informative | 100.0 | 1.4 | 98.6 | 0.7 | 90.3 | 70.5 | 9.0 |
| glm-5.3 | placebo | 98.6 | 100.0 | -1.4 | 34.7 | 49.3 | 67.1 | 0.3 |
| glm-5.3 | forged | 99.3 | 10.4 | 88.9 | 2.1 | 77.4 | 68.4 | 17.0 |
| qwen3.5-397b | none | 100.0 | 100.0 | 0.0 | 95.1 | 50.0 | 4.9 | 0.0 |
| qwen3.5-397b | informative | 100.0 | 45.1 | 54.9 | 40.3 | 76.4 | 8.1 | 1.0 |
| qwen3.5-397b | placebo | 100.0 | 100.0 | 0.0 | 93.1 | 50.0 | 6.9 | 0.0 |
| qwen3.5-397b | forged | 98.6 | 93.8 | 4.9 | 79.2 | 52.4 | 14.8 | 0.7 |
| qwen3.8-27b | none | 97.2 | 97.2 | 0.0 | 90.3 | 48.6 | 7.1 | 2.8 |
| qwen3.8-27b | informative | 91.7 | 51.4 | 40.3 | 43.8 | 53.5 | 11.7 | 20.8 |
| qwen3.8-27b | placebo | 94.4 | 95.1 | -0.7 | 88.9 | 47.2 | 7.3 | 5.2 |
| qwen3.8-27b | forged | 96.5 | 72.2 | 24.3 | 60.4 | 51.7 | 15.6 | 11.8 |
| pooled | none | 97.8 | 97.8 | 0.0 | 79.9 | 49.4 | 18.3 | 1.3 |
| pooled | informative | 97.9 | 46.7 | 51.2 | 39.9 | 68.9 | 22.8 | 7.6 |
| pooled | placebo | 97.4 | 97.8 | -0.4 | 75.7 | 49.0 | 22.9 | 1.8 |
| pooled | forged | 98.9 | 68.8 | 30.2 | 53.3 | 58.3 | 25.4 | 7.2 |

Pooled by language (%)

| Label | Language | Planted accepted | Silent error | Relay absent | Fact | Hedged | Attributed |
|---|---|---|---|---|---|---|---|
| none | en | 97.6 | 73.2 | 1.2 | 78.1 | 5.7 | 15.0 |
| none | hi | 97.9 | 77.4 | 1.5 | 80.8 | 3.7 | 14.0 |
| none | hinglish | 97.9 | 89.0 | 1.5 | 89.6 | 1.8 | 7.1 |
| informative | en | 34.2 | 27.7 | 12.6 | 43.5 | 0.4 | 43.5 |
| informative | hi | 52.4 | 42.9 | 8.5 | 50.7 | 1.9 | 38.8 |
| informative | hinglish | 53.6 | 49.1 | 10.3 | 62.8 | 0.6 | 26.3 |
| placebo | en | 97.3 | 65.8 | 1.9 | 69.2 | 6.1 | 22.8 |
| placebo | hi | 98.2 | 73.2 | 1.2 | 74.0 | 3.0 | 21.9 |
| placebo | hinglish | 97.9 | 88.1 | 1.5 | 87.9 | 1.2 | 9.4 |
| forged | en | 59.2 | 43.8 | 4.3 | 45.8 | 0.6 | 49.3 |
| forged | hi | 71.1 | 51.2 | 3.3 | 43.6 | 0.4 | 52.7 |
| forged | hinglish | 75.9 | 64.9 | 1.6 | 61.6 | 0.4 | 36.3 |
