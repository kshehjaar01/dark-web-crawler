# Scrapy settings for crawler project

BOT_NAME = "ethical_crawler"

SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"

# Respect robots.txt
ROBOTSTXT_OBEY = True

# Politeness
DOWNLOAD_DELAY = 2.0
CONCURRENT_REQUESTS = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# AutoThrottle
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 10.0

# Disable cookies
COOKIES_ENABLED = False

# Retries & redirects
RETRY_ENABLED = True
RETRY_TIMES = 3  # number of retries
HTTPREDIRECT_ENABLED = True

# Pipelines (order matters)
ITEM_PIPELINES = {
    "crawler.pipelines.FingerprintPipeline": 100,
    "crawler.pipelines.StructuredDataPipeline": 200,
    "crawler.pipelines.GraphPipeline": 300,
    "crawler.pipelines.JsonWriterPipeline": 400,
}

# Downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "crawler.middlewares.ErrorLoggingMiddleware": 543,
}

# Logging
LOG_LEVEL = "INFO"

# Where to keep SQLite DB and outputs
PROJECT_DATA_DIR = "../data"
FINGERPRINT_DB = "../data/fingerprints.db"
EDGES_CSV = "../data/edges.csv"
OUTPUT_JSON = "../data/output.json"
ERROR_LOG = "../data/errors.log"

# User-Agent
USER_AGENT = "ethical-crawler (+https://github.com/yourname/ethical-web-crawler)"


# Log level
LOG_LEVEL = "INFO"

# Identify bot in User-Agent — include contact info if appropriate
# Example: "ethical-crawler (+https://github.com/yourname/ethical-web-crawler)"
USER_AGENT = "ethical-crawler (+https://github.com/yourname/ethical-web-crawler)"

