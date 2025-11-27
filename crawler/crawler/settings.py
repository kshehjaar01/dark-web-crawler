# Scrapy settings for crawler project

BOT_NAME = "ethical_crawler"

SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"

# Respect robots.txt
ROBOTSTXT_OBEY = True

# Politeness
DOWNLOAD_DELAY = 2.0        # seconds between requests
CONCURRENT_REQUESTS = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# AutoThrottle to be polite
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0

# Disable cookies by default
COOKIES_ENABLED = False

# Pipelines
ITEM_PIPELINES = {
    "crawler.pipelines.JsonWriterPipeline": 300,
}

# Log level
LOG_LEVEL = "INFO"

# Identify bot in User-Agent — include contact info if appropriate
# Example: "ethical-crawler (+https://github.com/yourname/ethical-web-crawler)"
USER_AGENT = "ethical-crawler (+https://github.com/yourname/ethical-web-crawler)"

