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

# Phase 3: Innovate - Pearson correlation between price_cents and player_count
prices = df_merged['price_cents']
players = df_merged['player_count']

corr, p_value = stats.pearsonr(prices, players)

# Evaluate significance
is_significant = p_value < 0.05
rating = 85 if is_significant else 40

# Log to methodology_logbook.csv
with open(logbook_path, mode='a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow([
        "Pearson Correlation: Price vs Player Count",
        "Correlating base game price in cents with recent daily player count.",
        "price_cents, player_count",
        f"{p_value:.4f}",
        rating
    ])

# Generate Markdown Report
report_content = f"""# Data Science Report

**Date:** {today}
**Role:** Data Scientist

## Phase 3: Innovate

**Method:** Pearson Correlation
**Variables:** `price_cents` and `player_count`

### Results

- **Correlation Coefficient:** {corr:.4f}
- **p-value:** {p_value:.4f}

### Conclusion

"""
if is_significant:
    report_content += "The result is statistically significant (p < 0.05). There is a correlation between the price and player count.\n"
else:
    report_content += "The result is not statistically significant (p >= 0.05). This is a **Valuable Failure**. We do not reject the null hypothesis. Scientific honesty dictates we accept this lack of correlation without manipulating the data.\n"

with open(report_path, "w") as f:
    f.write(report_content)

print("Data Science tasks completed successfully.")
