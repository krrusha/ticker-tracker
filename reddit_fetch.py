"""
ticker-tracker/reddit_fetch.py

A read-only script that fetches public posts from Reddit finance subreddits
and extracts stock ticker mentions for trend analysis.

- No data is written to Reddit (no posts, votes, or comments)
- No personal user data is collected or stored
- Only public post titles and body text are read
- Intended for non-commercial personal/portfolio use only

Reddit subreddits accessed (read-only):
  r/wallstreetbets, r/stocks, r/investing
"""

import requests
import re
from collections import Counter
import time
 
# ── Config ──────────────────────────────────────────────────────────────────
HEADERS = {"User-Agent": "ticker-tracker/1.0 (personal project)"}
SUBREDDITS = ["wallstreetbets", "stocks", "investing"]
LIMIT = 25  # posts to fetch per subreddit (max 100)
 
# Common words that look like tickers but aren't — expand this list as needed
FALSE_POSITIVES = {
    "A", "I", "AM", "AN", "ARE", "AT", "BE", "BUT", "BY", "DO", "FOR",
    "GO", "HE", "IF", "IN", "IS", "IT", "ME", "MY", "NO", "OF", "ON",
    "OR", "SO", "TO", "UP", "US", "WE", "CEO", "IPO", "ETF", "GDP",
    "ATH", "ATL", "DD", "TL", "DR", "IMO", "WSB", "SEC", "FED", "USA",
    "USD", "ALL", "ANY", "NEW", "NOW", "ONE", "OUT", "OWN", "PAY", "PUT",
    "SAY", "SEE", "SET", "SHE", "THE", "TOO", "TWO", "WAY", "WHO", "WHY",
    "YES", "YET", "YOU", "AI", "EV", "UK", "EU", "PE", "VC", "API",
}
 
# ── Ticker extraction ────────────────────────────────────────────────────────
def extract_tickers(text):
    """
    Finds tickers in two formats:
      $AAPL  →  explicit cashtag (high confidence)
      AAPL   →  bare uppercase word 2-5 chars (lower confidence)
    """
    if not text:
        return []
 
    cashtags = re.findall(r'\$([A-Z]{1,5})\b', text.upper())
    bare = re.findall(r'\b([A-Z]{2,5})\b', text.upper())
    bare_filtered = [t for t in bare if t not in FALSE_POSITIVES]
 
    # Cashtags counted twice — they're a stronger signal
    return cashtags + cashtags + bare_filtered
 
# ── Reddit fetch ─────────────────────────────────────────────────────────────
def fetch_posts(subreddit, sort="hot", limit=LIMIT):
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?limit={limit}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        posts = r.json()["data"]["children"]
        return [p["data"] for p in posts]
    except Exception as e:
        print(f"  [error] r/{subreddit}: {e}")
        return []
 
# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("=" * 55)
    print("  Reddit Ticker Tracker — public .json endpoint")
    print("=" * 55)
 
    all_tickers = Counter()
    total_posts = 0
 
    for sub in SUBREDDITS:
        print(f"\nFetching r/{sub}...")
        posts = fetch_posts(sub)
        sub_tickers = Counter()
 
        for post in posts:
            text = f"{post.get('title', '')} {post.get('selftext', '')}"
            tickers = extract_tickers(text)
            sub_tickers.update(tickers)
 
        total_posts += len(posts)
        all_tickers.update(sub_tickers)
 
        top = sub_tickers.most_common(5)
        if top:
            print(f"  Top tickers: {', '.join(f'{t}({c})' for t, c in top)}")
        else:
            print("  No tickers found.")
 
        time.sleep(2)  # be polite — avoid hammering the endpoint
 
    print("\n" + "=" * 55)
    print(f"  Scanned {total_posts} posts across {len(SUBREDDITS)} subreddits")
    print("=" * 55)
    print("\nOverall top 15 tickers:\n")
    for ticker, count in all_tickers.most_common(15):
        bar = "█" * min(count, 40)
        print(f"  {ticker:<6} {bar} {count}")
 
if __name__ == "__main__":
    main()
