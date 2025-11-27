from crawler.spiders.example_spider import ExampleSpider
from scrapy.http import HtmlResponse, Request

def test_parse_extracts_title_and_links():
    html = b"""
    <html><head><title>Test page</title></head>
    <body>
      <a href="/about">About</a>
      <a href="https://example.com/contact">Contact</a>
      <a href="mailto:someone@example.com">mail</a>
    </body></html>
    """
    request = Request("https://example.com/")
    response = HtmlResponse(url="https://example.com/", request=request, body=html)
    spider = ExampleSpider()
    # parse yields an item (and potentially follow requests)
    results = list(spider.parse(response))
    assert len(results) >= 1
    item = results[0]
    assert item["title"] == "Test page"
    assert any("about" in link for link in item["links"])
    assert all(link.startswith("http") for link in item["links"])

