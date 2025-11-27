# dark-web-crawler
# Ethical Web Crawler

This repository is an educational, legal, and ethics-first web crawler built with Scrapy.

**Important:** This project is intended for legal, ethical use only. Do not use it to scrape or access systems without explicit permission. See `docs/ETHICS_GUIDELINES.md`.

## Features
- Scrapy-based spider that respects `robots.txt`
- Politeness: configurable delay, concurrency limits
- Output to JSON
- Dockerfile for reproducible runs
- Basic tests and CI workflow

## Quick start (local)
1. Create a Python virtualenv and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

