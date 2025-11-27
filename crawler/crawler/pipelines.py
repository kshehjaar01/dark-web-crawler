import os
import json
import csv
import sqlite3
import logging
from pathlib import Path
from typing import Dict, Any
from bs4 import BeautifulSoup
from scrapy.exceptions import DropItem
from crawler.utils import normalize_text, fingerprint_text

logger = logging.getLogger(__name__)

def ensure_data_dir(path: str):
    Path(path).mkdir(parents=True, exist_ok=True)

class FingerprintPipeline:
    """
    Compute fingerprint of page text and use a small SQLite DB to drop duplicates.
    """
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    @classmethod
    def from_crawler(cls, crawler):
        db_path = crawler.settings.get("FINGERPRINT_DB")
        ensure_data_dir(os.path.dirname(db_path) or ".")
        return cls(db_path)

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.db_path)
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS fingerprints (
                fp TEXT PRIMARY KEY,
                url TEXT,
                crawled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()
        spider.logger.info("Fingerprint DB ready at %s", self.db_path)

    def process_item(self, item: Dict[str, Any], spider):
        html = item.get("raw_html") or item.get("content") or ""
        normalized = normalize_text(html)
        fp = fingerprint_text(normalized)
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM fingerprints WHERE fp = ?", (fp,))
        if cur.fetchone():
            # Duplicate; drop
            spider.logger.info("Duplicate detected — dropping url: %s", item.get("url"))
            raise DropItem(f"Duplicate content: {item.get('url')}")
        # Insert new fingerprint
        cur.execute("INSERT INTO fingerprints (fp, url) VALUES (?, ?)", (fp, item.get("url")))
        self.conn.commit()
        # attach fingerprint to item for downstream pipelines
        item["fingerprint"] = fp
        return item

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

class StructuredDataPipeline:
    """
    Extract structured pieces of data (title, meta description, h1s, JSON-LD).
    Normalizes HTML and attaches structured fields to item.
    """
    def process_item(self, item, spider):
        html = item.get("raw_html") or item.get("content") or ""
        soup = BeautifulSoup(html, "lxml")
        # Title
        title = (soup.title.string.strip() if soup.title else "") if html else ""
        # Meta description
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""
        # H1 tags
        h1s = [h.get_text(strip=True) for h in soup.find_all("h1")]
        # JSON-LD structured data
        json_ld = []
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                parsed = json.loads(script.string)
                json_ld.append(parsed)
            except Exception:
                continue
        # Attach
        item.setdefault("structured", {})
        item["structured"].update({
            "title": title,
            "meta_description": description,
            "h1s": h1s,
            "json_ld": json_ld
        })
        return item

class GraphPipeline:
    """
    Record directed edges (from_url -> to_url) into a CSV edges file.
    The spider must include 'links' (list of absolute urls) in item.
    """
    def __init__(self, edges_csv):
        self.edges_csv = edges_csv
        self.file = None
        self.writer = None
        self._seen_edges = set()

    @classmethod
    def from_crawler(cls, crawler):
        edges_csv = crawler.settings.get("EDGES_CSV")
        ensure_data_dir(os.path.dirname(edges_csv) or ".")
        return cls(edges_csv)

    def open_spider(self, spider):
        # Open CSV in append mode but ensure header exists
        header_needed = not Path(self.edges_csv).exists()
        self.file = open(self.edges_csv, "a", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)
        if header_needed:
            self.writer.writerow(["from", "to"])
        spider.logger.info("Graph edges will be written to %s", self.edges_csv)

    def process_item(self, item, spider):
        from_url = item.get("url")
        links = item.get("links") or []
        for to in links:
            edge = (from_url, to)
            if edge in self._seen_edges:
                continue
            self._seen_edges.add(edge)
            try:
                self.writer.writerow([from_url, to])
            except Exception as e:
                logger.exception("Failed to write edge %s -> %s: %s", from_url, to, e)
        return item

    def close_spider(self, spider):
        if self.file:
            self.file.close()

class JsonWriterPipeline:
    """
    Write items to a JSON array output file (append-safe by streaming).
    Drops any 'raw_html' if present to keep JSON smaller.
    """
    def __init__(self, output_path):
        self.output_path = output_path
        self.file = None
        self.first = True

    @classmethod
    def from_crawler(cls, crawler):
        output_path = crawler.settings.get("OUTPUT_JSON")
        ensure_data_dir(os.path.dirname(output_path) or ".")
        return cls(output_path)

    def open_spider(self, spider):
        # Stream: create/truncate file at start
        self.file = open(self.output_path, "w", encoding="utf-8")
        self.file.write("[\n")
        self.first = True
        spider.logger.info("JSON output will be written to %s", self.output_path)

    def process_item(self, item, spider):
        # Remove raw_html to reduce size if present
        item_to_write = dict(item)
        if "raw_html" in item_to_write:
            item_to_write.pop("raw_html", None)
        line = json.dumps(item_to_write, ensure_ascii=False)
        if not self.first:
            self.file.write(",\n")
        self.file.write(line)
        self.first = False
        return item

    def close_spider(self, spider):
        self.file.write("\n]\n")
        self.file.close()

