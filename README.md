# Ticker Tracker

A non-commercial personal project that tracks stock ticker mentions 
across Reddit finance subreddits in real time.

## What it does
- Polls public posts from r/wallstreetbets, r/stocks, r/investing, and others
- Extracts stock ticker symbols ($AAPL, TSLA, etc.) from post titles and body text
- Scores sentiment of surrounding text (bullish/bearish/neutral)
- Aggregates mention counts into a time-series dashboard

## Data usage
- Read-only access to public Reddit posts
- No user data collected or stored
- No Reddit content republished verbatim
- Aggregated/derived data only (mention counts, sentiment scores)

## Stack
- Python (PRAW / requests)
- SQLite for time-series storage
- React frontend dashboard (in progress)

## Status
In development. Reddit API access pending approval.

## Non-commercial
This is a personal portfolio project. No ads, no monetization, no commercial use.
