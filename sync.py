name: Daily Freight Notion Sync

on:
  schedule:
    # Runs every day at 11:00 UTC (7:00 AM Eastern Time)
    - cron: '0 11 * * *'
  workflow_dispatch: # Allows you to click a button to run it manually anytime

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository code
        uses: actions/checkout@v4

      - name: Set up Python environment
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install website scraping tools
        run: pip install beautifulsoup4 requests

      - name: Execute Sync Script
        run: python sync.py
