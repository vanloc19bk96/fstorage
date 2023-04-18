import json

from source.constants import PROXY_STORAGE_DB
from utils.log import log
import redis


@log
class ProxyStorage:
    def __init__(self, config):
        self.redis = None
        self.key = config[PROXY_STORAGE_DB]
        config_without_key = {k: v for k, v in config.items() if k != PROXY_STORAGE_DB}
        self.connect(config_without_key)
        self.logger.info(f"Connected to proxy storage!")

    def __enter__(self):
        return self

    def connect(self, config):
        pool = redis.ConnectionPool(**config)
        self.redis = redis.Redis(connection_pool=pool)

    def get_all(self):
        proxies = self.redis.lrange(self.key, 0, -1)

        return [
            json.loads(proxy) for proxy in proxies
        ]

    def add_proxies(self, proxies):
        self.logger.info(f"Overriding existing proxies {proxies}")
        if len(proxies) != 0:
            self.redis.delete(self.key)
            self.redis.lpush(self.key, *proxies)

    def pop_proxy(self):
        self.logger.info("Deleting proxy!")
        self.redis.lpop(self.key)

    def __exit__(self, exc_type, exc_val, exc_tb):
        client_id = self.redis.client_id()
        self.redis.client_kill_filter(
            _id=client_id
        )


config = {
    "storage_key": "proxy",
    "host": "localhost",
    "port": 6379,
    "db": 0
}

# proxy = ProxyStorage(config)
# proxy.add_proxies([])
# proxy.get_all()
