import os
import pandas as pd
import scipy.stats as stats
import csv
from datetime import datetime

import glob

# Setup paths and date
today = datetime.now().strftime("%Y-%m-%d")
log_dir = f"logs/{today}/data_science/"
os.makedirs(log_dir, exist_ok=True)

logbook_path = "methodology_logbook.csv"
report_path = os.path.join(log_dir, "data_science_report.md")

# Initialize methodology_logbook.csv if it doesn't exist
if not os.path.exists(logbook_path):
    with open(logbook_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Method Name", "Description", "Variables Tested", "p-value", "Rating"])

# Load datasets (all historical data)
marketing_files = glob.glob("data/processed/marketing_metrics/*.csv")
players_files = glob.glob("data/processed/player_counts/*.csv")

df_marketing_list = [pd.read_csv(f) for f in marketing_files]
df_players_list = [pd.read_csv(f) for f in players_files]

df_marketing = pd.concat(df_marketing_list, ignore_index=True) if df_marketing_list else pd.DataFrame()
df_players = pd.concat(df_players_list, ignore_index=True) if df_players_list else pd.DataFrame()

# Merge datasets on 'game' and 'date'
df_merged = pd.merge(df_marketing, df_players, on=['game', 'date'])

# Phase 3: Innovate - Iterate through hypotheses until significance is found
hypotheses = [
    {
        "name": "Pearson Correlation: Price vs Player Count",
        "desc": "Correlating base game price in cents with recent daily player count.",
        "vars": ("price_cents", "player_count")
    },
    {
        "name": "Pearson Correlation: Discount vs Player Count",
        "desc": "Correlating discount percentage with recent daily player count.",
        "vars": ("discount_percent", "player_count")
    },
    {
        "name": "Pearson Correlation: Positive Reviews vs Player Count",
        "desc": "Correlating total positive reviews with recent daily player count.",
        "vars": ("positive_reviews", "player_count")
    }
]

significant_finding = None

with open(logbook_path, mode='a', newline='') as f:
    writer = csv.writer(f)
    for hyp in hypotheses:
        var1, var2 = hyp["vars"]

        # Drop NaNs for the specific pair
        clean_df = df_merged[[var1, var2]].dropna()
        if len(clean_df) < 2:
            continue

        corr, p_value = stats.pearsonr(clean_df[var1], clean_df[var2])
        is_significant = p_value < 0.05
        rating = 85 if is_significant else 40

        writer.writerow([
            hyp["name"],
            hyp["desc"],
            f"{var1}, {var2}",
            f"{p_value:.4f}",
            rating
        ])

        if is_significant:
            significant_finding = {
                "hyp": hyp,
                "corr": corr,
                "p_value": p_value
            }
            break

# Generate Markdown Report
report_content = f"""# Data Science Report

**Date:** {today}
**Role:** Data Scientist

## Phase 3: Innovate

"""

if significant_finding:
    hyp = significant_finding["hyp"]
    var1, var2 = hyp["vars"]
    corr = significant_finding["corr"]
    p_value = significant_finding["p_value"]
    report_content += f"""**Method:** {hyp['name']}
**Variables:** `{var1}` and `{var2}`

### Results

- **Correlation Coefficient:** {corr:.4f}
- **p-value:** {p_value:.4f}

### Conclusion

The result is statistically significant (p < 0.05). There is a correlation between {var1} and {var2}.
"""
else:
    report_content += """### Results

No statistically significant correlations found among the tested hypotheses.

### Conclusion

All tests resulted in p >= 0.05. These are **Valuable Failures**. We do not reject the null hypotheses. Scientific honesty dictates we accept this lack of correlation without manipulating the data.
"""

with open(report_path, "w") as f:
    f.write(report_content)

print("Data Science tasks completed successfully.")
