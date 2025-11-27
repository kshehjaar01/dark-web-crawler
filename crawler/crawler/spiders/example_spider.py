import scrapy
from urllib.parse import urljoin, urlparse
from w3lib.url import canonicalize_url

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com/"]

    custom_settings = {
        "CLOSESPIDER_PAGECOUNT": 200  # safety limit per run
    }

    def parse(self, response):
        # raw_html used for fingerprinting
        raw_html = response.text

        # extract links (absolute)
        links = []
        for href in response.css("a::attr(href)").getall():
            href = href.strip()
            if not href:
                continue
            absolute = urljoin(response.url, href)
            parsed = urlparse(absolute)
            # Only http(s) links
            if parsed.scheme in ("http", "https"):
                # optionally canonicalize to reduce duplicates
                absolute = canonicalize_url(absolute)
                links.append(absolute)

        item = {
            "url": response.url,
            "raw_html": raw_html,
            "links": links,
        }

        # yield item for pipelines (structured data extraction, fingerprinting, graph, output)
        yield item

        # Follow same-domain links
        for link in links:
            parsed = urlparse(link)
            # strict domain check: endswith allowed domain
            if any(parsed.netloc.endswith(d) for d in self.allowed_domains):
                yield scrapy.Request(url=link, callback=self.parse)
