#!/usr/bin/env bash
set -e
cd crawler
scrapy crawl example -o ../output.json
echo "Saved results to output.json"

