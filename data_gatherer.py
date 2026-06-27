import json
import os
import subprocess
import shutil
import requests
import pandas as pd
from datetime import datetime

# Configuration
GAMES = {
    "Rust": "252490",
    "SCUM": "513710",
    "DayZ": "221100",
    "Project Zomboid": "108600",
    "7 Days to Die": "251570"
}
PERFORMANCE_KEYWORDS = ["lag", "fps", "drop", "stutter", "performance"]

def get_current_date():
    try:
        date_str = subprocess.check_output(["date", "+%Y-%m-%d"]).decode("utf-8").strip()
        return date_str
    except Exception as e:
        print(f"Error getting date: {e}")
        return datetime.now().strftime("%Y-%m-%d")

CURRENT_DATE = get_current_date()

# Directories
RAW_DIR = os.path.join("data", "raw", CURRENT_DATE)
PROCESSED_DIR = os.path.join("data", "processed")
PLAYER_COUNTS_DIR = os.path.join(PROCESSED_DIR, "player_counts")
SENTIMENT_DIR = os.path.join(PROCESSED_DIR, "performance_sentiment")

def setup_directories():
    for d in [RAW_DIR, PLAYER_COUNTS_DIR, SENTIMENT_DIR]:
        os.makedirs(d, exist_ok=True)

def fetch_player_count(appid):
    url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "response" in data and "player_count" in data["response"]:
            return data["response"]["player_count"]
    return None

def fetch_reviews(appid, num_per_page=100):
    # Fetch recent reviews
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&filter=recent&num_per_page={num_per_page}&language=english"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("reviews", [])
    return []

def gather_raw_data():
    raw_data = {}
    for game, appid in GAMES.items():
        print(f"Gathering raw data for {game}...")
        player_count = fetch_player_count(appid)
        reviews = fetch_reviews(appid)

        game_data = {
            "player_count": player_count,
            "reviews": reviews,
            "appid": appid
        }

        # Save raw data
        raw_file = os.path.join(RAW_DIR, f"{game.replace(' ', '_')}_raw.json")
        with open(raw_file, "w", encoding="utf-8") as f:
            json.dump(game_data, f, indent=4)

        raw_data[game] = game_data
    return raw_data

def process_data(raw_data):
    # Process Player Counts
    player_counts = []
    for game, data in raw_data.items():
        if data["player_count"] is not None:
            player_counts.append({
                "date": CURRENT_DATE,
                "game": game,
                "player_count": data["player_count"]
            })

    if player_counts:
        df_pc = pd.DataFrame(player_counts)
        pc_file = os.path.join(PLAYER_COUNTS_DIR, f"{CURRENT_DATE}_player_counts.csv")
        df_pc.to_csv(pc_file, index=False)
        print(f"Saved processed player counts to {pc_file}")

    # Process Reviews for Performance Sentiment
    for game in ["Rust", "SCUM"]:
        if game in raw_data:
            reviews = raw_data[game]["reviews"]
            sentiment_data = []

            for review in reviews:
                text = review.get("review", "").lower()
                has_perf_issue = any(keyword in text for keyword in PERFORMANCE_KEYWORDS)

                sentiment_data.append({
                    "date": CURRENT_DATE,
                    "game": game,
                    "recommendationid": review.get("recommendationid"),
                    "voted_up": review.get("voted_up"),
                    "has_performance_complaint": has_perf_issue,
                    "review_length": len(text)
                })

            if sentiment_data:
                df_sent = pd.DataFrame(sentiment_data)
                sent_file = os.path.join(SENTIMENT_DIR, f"{CURRENT_DATE}_{game}_sentiment.csv")
                df_sent.to_csv(sent_file, index=False)
                print(f"Saved processed sentiment for {game} to {sent_file}")

def cleanup_raw_data():
    if os.path.exists(RAW_DIR):
        print(f"Cleaning up temporary raw data in {RAW_DIR}...")
        shutil.rmtree(RAW_DIR)

if __name__ == "__main__":
    setup_directories()
    raw_data = gather_raw_data()
    process_data(raw_data)
    cleanup_raw_data()
    print("Data Gatherer pipeline completed successfully.")
