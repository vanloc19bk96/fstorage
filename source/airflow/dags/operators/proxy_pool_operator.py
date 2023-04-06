from concurrent.futures import ThreadPoolExecutor

from source.airflow.constants import PROXY_KEY, URL_KEY, TESTING_URL_KEY, HEALTHCHECK_KEY, NUMBER_OF_PROXIES, \
    PROXY_STORAGE_KEY, PROXY_STORAGE_DB_KEY, NUMBER_OF_WORKERS, LIMIT_PROXIES
from source.crawler.proxypool.proxy_crawler import ProxyCrawler
from source.crawler.proxypool.proxy_storage import ProxyStorage
from source.crawler.proxypool.proxy_validator import ProxyValidator
from utils.parser import ConfigParser
from utils.retry import RetryOnException as retry
import json


class ProxyPoolOperator():
    # @apply_defaults
    def __init__(self, config_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = ConfigParser.from_args(config_path)

    @retry(5)
    def execute(self, context):
        crawler_url = self.config[PROXY_KEY][URL_KEY]
        testing_url = self.config[PROXY_KEY][TESTING_URL_KEY]
        healthcheck = self.config[PROXY_KEY][HEALTHCHECK_KEY]
        number_of_proxies = self.config[PROXY_KEY][NUMBER_OF_PROXIES]
        redis_config = self.config[PROXY_KEY][PROXY_STORAGE_KEY]
        storage_key = redis_config[PROXY_STORAGE_DB_KEY]

        proxy_crawler = ProxyCrawler(crawler_url)
        proxy_validator = ProxyValidator(testing_url, healthcheck)

        proxy_stream = proxy_crawler.get_proxy_stream(number_of_proxies)

        max_workers = self.config[PROXY_KEY][NUMBER_OF_WORKERS]
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            results = executor.map(proxy_validator.validate, proxy_stream)
            valid_proxies = filter(lambda x: x.is_valid is True, results)
            sorted_valid_proxies = sorted(
                valid_proxies, key=lambda x: x.health, reverse=True
            )
        limit_proxies = self.config[PROXY_KEY][LIMIT_PROXIES]
        with ProxyStorage(storage_key, redis_config) as storage:
            storage.add_proxies(
                [
                    json.dumps(record) for record in sorted_valid_proxies[:limit_proxies]
                ]
            )


proxy = ProxyPoolOperator("../../../config.yaml")
proxy.execute(None)
