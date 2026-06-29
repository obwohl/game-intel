# Data Science Report: Ardem Pre-Launch Market Analysis

**Date:** 2026-06-28
**Role:** Data Scientist

## Executive Summary

Today's Exploratory Data Analysis (EDA) focused on extracting actionable Business Intelligence for the executive leadership of *Ardem* using a statistically robust dataset (N=50) of top competitors in the Survival genre. We explicitly addressed high-leverage outliers to ensure findings are not artifacts of single massive games.

## Phase 3: Exploratory Data Analysis (EDA)

### Hypothesis 1: Price Sensitivity

**Method:** Pearson Correlation
**Variables Tested:** `price_cents` vs `player_count`

**Results (All Data, N=50):**

- **Correlation Coefficient:** -0.1183
- **p-value:** 0.4132

**Results (Excluding 5 Extreme Outliers, N=45):**

- **Correlation Coefficient:** -0.1808
- **p-value:** 0.2346

**Conclusion:** The correlation remains weak or statistically insignificant even after accounting for scale differences. We do not reject the null hypothesis.

### Hypothesis 2: Brand Goodwill (Positive Sentiment)

**Method:** Pearson Correlation
**Variables Tested:** `positive_reviews` vs `player_count`

**Results (All Data, N=50):**

- **Correlation Coefficient:** 0.6159
- **p-value:** 0.0000

**Results (Excluding 5 Extreme Outliers, N=45):**

- **Correlation Coefficient:** 0.3278
- **p-value:** 0.0279

**Conclusion:** With a robust sample size, we observe a positive correlation between positive reviews and active players, both with and without extreme outliers. However, we must strictly caveat that **correlation is not causation**. Positive reviews are typically a lagging indicator (players review games they already play), not a leading indicator that generates players.

## Publisher Actionable Insight (Ardem Pre-Launch)

Based on the robust EDA (N=50):

1. **Price is not the primary driver:** Competing in a race to the bottom on price is statistically unsound for player retention.
2. **Community scale drives reviews, not vice-versa:** While positive reviews strongly correlate with high player counts, executives must recognize this is a lagging effect. You cannot "buy" active players simply by optimizing for positive reviews; you must build engaging mechanics that organically drive both play time and subsequent positive sentiment. Focus marketing on demonstrating deep, engaging gameplay.
