import json

from utils.log import log
import redis


@log
class ProxyStorage:
    def __init__(self, key, config):
        self._redis = None
        self.key = key
        self.connect(config)
        self.logger.info(f"Connected to proxy storage!")

    def connect(self, config):
        connection_pool = redis.ConnectionPool(**config)
        self._redis = redis.Redis(connection_pool=connection_pool)

    def get_all(self):
        proxies = self.redis.lrange(self.redis, 0, -1)

        return [
            json.load(proxy) for proxy in proxies
        ]

    def add_proxies(self, proxies):
        self.loger.info(f"Overriding existing proxies {proxies}")
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



