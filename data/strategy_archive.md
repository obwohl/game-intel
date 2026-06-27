# Archived Data Strategy: Operations & Retention

*Date Archived:* 2026-06-27
*Note:* This strategy was developed for post-launch operational analysis but was archived prior to Ardem's release as the executive focus shifted to pre-launch marketing, influencer impact, and hype generation.

## Foundational BI Datasets

### 1. Player Counts (`player_counts.csv`)

- **What it is:** Daily snapshots of concurrent player bases for all major competitors.
- **Data Science Application:** Time-series analysis and drop-off modeling. The Data Scientist will track how long competitor games hold their player bases after a major patch or "wipe."
- **Executive BI Value:** Executives can see a mathematically proven "decay curve" for survival games. For example, if the data proves that 60% of players leave within 14 days of an update across all competitors, Ardem's executives can plan their post-launch content roadmap to drop smaller, more frequent updates (e.g., every 10 days) to interrupt that decay curve and steal market share.

### 2. BI Summary Stats (`bi_summary.csv`)

- **What it is:** High-level totals of positive/negative reviews and overall sentiment scores.
- **Data Science Application:** Correlation analysis between community satisfaction and player retention. The Data Scientist can determine if a sudden influx of negative reviews historically precedes a mass exodus of players, or if players keep playing despite complaining.
- **Executive BI Value:** Risk management. If the data shows that the market tolerates certain types of bugs but harshly punishes others (reflected in review bombs), Ardem's leadership knows exactly where to allocate QA and development budgets before launch.

### 3. Performance Sentiment Index (`<Game>_sentiment.csv`)

- **What it is:** Detailed logs of recent reviews flagged specifically for performance issues (lag, stutter, fps drops).
- **Data Science Application:** The Data Scientist can perform regression analysis to see how strongly "technical debt" impacts the bottom line. They can quantify exactly how much a 10% increase in performance complaints hurts a competitor's player count.
- **Executive BI Value:** The "Server Death" phenomenon was identified by the News Agent as a major risk. By quantifying this, the Data Scientist can tell Ardem's executives: *"Competitor data proves that poor server optimization during large-scale building leads to a 35% faster player churn. We must prioritize server infrastructure over adding new weapons."*
