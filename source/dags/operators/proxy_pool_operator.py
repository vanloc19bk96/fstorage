import json

from concurrent.futures import ThreadPoolExecutor

from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

from source.constants import PROXY, URL, TESTING_URL, HEALTHCHECK, NUMBER_OF_PROXIES, \
    PROXY_STORAGE, NUMBER_OF_WORKERS, LIMIT_PROXIES
from source.crawler.proxypool.proxy_crawler import ProxyCrawler
from source.crawler.proxypool.proxy_storage import ProxyStorage
from source.crawler.proxypool.proxy_validator import ProxyValidator
from utils.constants import CRAWLER_CONFIG_PATH
from utils.log import log
from utils.parser import ConfigParser
from utils.retry import RetryOnException as retry


@log
class ProxyPoolOperator(BaseOperator):
    @apply_defaults
    def __init__(self, config, *args, **kwargs):
        self.config = config
        super().__init__(*args, **kwargs)

    @retry(5)
    def execute(self, context):
        crawler_url = self.config[PROXY][URL]
        testing_url = self.config[PROXY][TESTING_URL]
        healthcheck = self.config[PROXY][HEALTHCHECK]
        number_of_proxies = self.config[PROXY][NUMBER_OF_PROXIES]
        redis_config = self.config[PROXY][PROXY_STORAGE]

        proxy_crawler = ProxyCrawler(crawler_url)
        proxy_validator = ProxyValidator(testing_url, healthcheck)

        proxy_stream = proxy_crawler.get_proxy_stream(number_of_proxies)

        max_workers = self.config[PROXY][NUMBER_OF_WORKERS]
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(proxy_validator.validate, proxy_stream)
            valid_proxies = filter(lambda x: x.is_valid is True, results)
            sorted_valid_proxies = sorted(
                valid_proxies, key=lambda x: x.health, reverse=True
            )

        limit_proxies = self.config[PROXY][LIMIT_PROXIES]
        with ProxyStorage(redis_config) as storage:
            storage.add_proxies(
                [
                    json.dumps(record.proxy)
                    for record in sorted_valid_proxies[:limit_proxies]
                ]
            )


# config = ConfigParser.from_args(CRAWLER_CONFIG_PATH)
# operator = ProxyPoolOperator(config)
# operator.execute(None)
