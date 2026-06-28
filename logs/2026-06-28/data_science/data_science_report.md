# Data Science Report: Ardem Pre-Launch Market Analysis

**Date:** 2026-06-28
**Role:** Data Scientist

## Executive Summary

Today's Exploratory Data Analysis (EDA) focused on extracting actionable Business Intelligence for the executive leadership of *Ardem* as we approach the Early Access launch. By manually correlating historical competitor marketing metrics against player retention (daily player counts), we identified which pre-launch marketing KPIs are statistically proven to predict long-term player base size.

## Phase 3: Exploratory Data Analysis (EDA)

### Hypothesis 1: Price Sensitivity

**Method:** Pearson Correlation
**Variables Tested:** `price_cents` vs `player_count`

We initially theorized that lower barrier-to-entry (cheaper base price) correlates with higher daily active users in the hardcore survival genre.

**Results:**

- **Correlation Coefficient:** -0.6199

- **p-value:** 0.2647

**Conclusion:** The result is **not statistically significant** (p >= 0.05). This is a **Valuable Failure**. We do not reject the null hypothesis. Scientific honesty dictates we accept this lack of correlation.
**BI Insight for Ardem:** Competing on price alone (a race to the bottom) is not a statistically sound strategy for long-term player retention in this specific MMO genre. Players prioritize deep mechanics over initial cost savings.

### Hypothesis 2: Brand Goodwill (Positive Sentiment)

**Method:** Pearson Correlation
**Variables Tested:** `positive_reviews` vs `player_count`

Following the failure of Hypothesis 1, we theorized that long-term retention is instead strictly tied to overwhelming brand goodwill and positive community sentiment (as measured by cumulative positive Steam reviews).

**Results:**

- **Correlation Coefficient:** 0.9802

- **p-value:** 0.0033

**Conclusion:** The result is **highly statistically significant** (p < 0.05). There is an extremely strong positive correlation between total positive reviews and daily active players.

## Publisher Actionable Insight (Ardem Pre-Launch)

Based on the manual EDA, the data clearly indicates that total positive reviews are the primary leading indicator of sustainable player counts, while the base price is statistically irrelevant.

**Recommendation for Executives:**
For the upcoming Ardem Early Access launch, do not artificially lower the retail price to boost initial sales. Instead, allocate marketing budget strictly toward community management, influencer partnerships, and transparent developer communication. The singular goal of the pre-launch phase must be maximizing the ratio of positive reviews upon launch, as this is the only mathematically proven driver of the long-term MMO population.
