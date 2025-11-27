import scrapy
from crawler.items import PageItem
from urllib.parse import urljoin, urlparse

class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["https://example.com/"]

    custom_settings = {
        "CLOSESPIDER_PAGECOUNT": 50  # safety: stop after limited pages
    }

    def parse(self, response):
        item = PageItem()
        item["url"] = response.url
        item["title"] = response.xpath("//title/text()").get(default="").strip()
        links = []
        for href in response.css("a::attr(href)").getall():
            href = href.strip()
            if not href:
                continue
            absolute = urljoin(response.url, href)
            parsed = urlparse(absolute)
            # Only include http[s] links
            if parsed.scheme in ("http", "https"):
                links.append(absolute)
        item["links"] = links
        yield item

        # follow links within allowed domains only
        for link in links:
            parsed = urlparse(link)
            if parsed.netloc.endswith("example.com"):
                yield response.follow(link, callback=self.parse)

