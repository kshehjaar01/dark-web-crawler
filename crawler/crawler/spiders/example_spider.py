import logging
from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

logger = logging.getLogger(__name__)

class ErrorLoggingMiddleware(RetryMiddleware):
    """
    Extends Scrapy's RetryMiddleware to log errors to a file via spider.logger
    """
    def __init__(self, settings):
        super().__init__(settings)
        self.max_retry_times = settings.getint('RETRY_TIMES', 3)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_response(self, request, response, spider):
        # If response status is 4xx/5xx, log it
        if response.status >= 400:
            spider.logger.warning("HTTP %s on %s", response.status, response.url)
        return super().process_response(request, response, spider)

    def process_exception(self, request, exception, spider):
        spider.logger.error("Exception for %s: %s", request.url, exception)
        return super().process_exception(request, exception, spider)
