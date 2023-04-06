from airflow.models.baseoperator import BaseOperator
from airflow.utils.decorators import apply_defaults

from source.airflow.constants import PROXY_KEY, URL_KEY, TESTING_URL_KEY, HEALTHCHECK_KEY, NUMBER_OF_PROXIES, \
    PROXY_STORAGE_KEY, PROXY_STORAGE_DB_KEY, PROXY_SERVICE_KEY
from source.crawler.proxypool.proxy_crawler import ProxyCrawler
from source.crawler.proxypool.proxy_storage import ProxyStorage
from source.crawler.proxypool.proxy_validator import ProxyValidator
from utils.parser import ConfigParser
from utils.retry import RetryOnException as retry


class ProxyPoolOperator(BaseOperator):
    # @apply_defaults
    def __init__(self, config_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = ConfigParser.from_args(config_path)
        print(self.config["proxy"])

    @retry(5)
    def execute(self, context):
        # redis_config = {
        #     "host": "localhost",
        #     "port": 6379,
        #     "db": 0
        # }
        #
        # key = "abc"

        # url = "https://free-proxy-list.net/"
        crawler_url = self.config[PROXY_KEY][URL_KEY]
        testing_url = self.config[PROXY_KEY][TESTING_URL_KEY]
        healthcheck = self.config[PROXY_KEY][HEALTHCHECK_KEY]
        number_of_proxies = self.config[PROXY_KEY][NUMBER_OF_PROXIES]
        storage_key = self.config[PROXY_KEY][PROXY_STORAGE_DB_KEY]
        redis_config = self.config[PROXY_KEY][PROXY_SERVICE_KEY]

        proxy_crawler = ProxyCrawler(crawler_url)
        proxy_validator = ProxyValidator(testing_url, healthcheck)
        proxy_storage = ProxyStorage(storage_key, redis_config)

        proxy_stream = proxy_crawler.get_proxy_stream(number_of_proxies)

        validated_proxies = list(map(proxy_validator.validate, proxy_stream))


proxy = ProxyPoolOperator("../../../config.yaml")
