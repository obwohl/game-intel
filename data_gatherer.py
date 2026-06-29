import json
import os
import subprocess
import shutil
import requests
import pandas as pd
from datetime import datetime
import time

# Configuration

def get_top_survival_games(limit=50):
    url = "https://steamspy.com/api.php?request=tag&tag=Survival"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Sort by ccu (if available) to get the most relevant ones
            games = sorted(
                [x for x in data.values() if isinstance(x, dict)],
                key=lambda x: int(x.get('ccu') or 0),
                reverse=True
            )[:limit]
            return {g['name']: str(g['appid']) for g in games if 'name' in g and 'appid' in g}
    except Exception as e:
        print(f"Error fetching top survival games: {e}")
    return {}

DEFAULT_GAMES = {
    "Rust": "252490",
    "SCUM": "513710",
    "DayZ": "221100",
    "Project Zomboid": "108600",
    "7 Days to Die": "251570"
}

GAMES = get_top_survival_games() or DEFAULT_GAMES

MARKETING_KEYWORDS = ["hype", "early access", "trailer", "streamer", "tiktok", "youtube", "worth it", "twitch"]

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
MARKETING_DIR = os.path.join(PROCESSED_DIR, "marketing_metrics")
PLAYER_COUNTS_DIR = os.path.join(PROCESSED_DIR, "player_counts")
HYPE_DIR = os.path.join(PROCESSED_DIR, "hype_sentiment")

def setup_directories():
    for d in [RAW_DIR, MARKETING_DIR, HYPE_DIR, PLAYER_COUNTS_DIR]:
        os.makedirs(d, exist_ok=True)

def fetch_steamspy_data(appid):
    url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching SteamSpy data for {appid}: {e}")
    return {}

def fetch_reviews(appid, num_per_page=100):
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1&filter=recent&num_per_page={num_per_page}&language=english"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("reviews", [])
    except Exception as e:
        print(f"Error fetching reviews for {appid}: {e}")
    return []

def gather_raw_data():
    raw_data = {}
    for game, appid in GAMES.items():
        print(f"Gathering raw marketing data for {game}...")
        steamspy_data = fetch_steamspy_data(appid)
        time.sleep(1) # Be polite to SteamSpy API
        reviews = fetch_reviews(appid)

        game_data = {
            "steamspy": steamspy_data,
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
# Process Marketing Metrics and Player Counts from SteamSpy
    marketing_metrics = []
    player_counts = []
    for game, data in raw_data.items():
        if "steamspy" in data and data["steamspy"]:
            spy = data["steamspy"]
            marketing_metrics.append({
                "date": CURRENT_DATE,
                "game": game,
                "owners_range": spy.get("owners"),
                "price_cents": spy.get("price"),
                "initialprice_cents": spy.get("initialprice"),
                "discount_percent": spy.get("discount"),
                "positive_reviews": spy.get("positive"),
                "negative_reviews": spy.get("negative"),
                "top_tags": json.dumps(list(spy["tags"].keys())[:5]) if isinstance(spy.get("tags"), dict) else ""
            })
            if "ccu" in spy:
                player_counts.append({
                    "date": CURRENT_DATE,
                    "game": game,
                    "player_count": spy.get("ccu") or 0
                })

    if marketing_metrics:
        df_mkt = pd.DataFrame(marketing_metrics)
        mkt_file = os.path.join(MARKETING_DIR, f"{CURRENT_DATE}_marketing_metrics.csv")
        df_mkt.to_csv(mkt_file, index=False)
        print(f"Saved processed marketing metrics to {mkt_file}")

    if player_counts:
        df_pc = pd.DataFrame(player_counts)
        pc_file = os.path.join(PLAYER_COUNTS_DIR, f"{CURRENT_DATE}_player_counts.csv")
        df_pc.to_csv(pc_file, index=False)
        print(f"Saved processed player counts to {pc_file}")

    # Process Reviews for Hype & Influencer Sentiment
    for game in GAMES.keys():
        if game in raw_data:
            reviews = raw_data[game]["reviews"]
            sentiment_data = []

            for review in reviews:
                text = (review.get("review") or "").lower()
                hype_mentions = [kw for kw in MARKETING_KEYWORDS if kw in text]

                if hype_mentions:
                    sentiment_data.append({
                        "date": CURRENT_DATE,
                        "game": game,
                        "recommendationid": review.get("recommendationid"),
                        "voted_up": review.get("voted_up"),
                        "hype_keywords_found": ", ".join(hype_mentions),
                        "review_length": len(text)
                    })

            if sentiment_data:
                df_sent = pd.DataFrame(sentiment_data)
                sent_file = os.path.join(HYPE_DIR, f"{CURRENT_DATE}_{game.replace(' ', '_')}_hype_sentiment.csv")
                df_sent.to_csv(sent_file, index=False)
                print(f"Saved hype sentiment for {game} to {sent_file}")
            else:
                print(f"No hype keywords found for {game} today.")

def cleanup_raw_data():
    if os.path.exists(RAW_DIR):
        print(f"Cleaning up temporary raw data in {RAW_DIR}...")
        shutil.rmtree(RAW_DIR)

if __name__ == "__main__":
    setup_directories()
    raw_data = gather_raw_data()
    process_data(raw_data)
    cleanup_raw_data()
    print("Data Gatherer (Marketing Focus) pipeline completed successfully.")
