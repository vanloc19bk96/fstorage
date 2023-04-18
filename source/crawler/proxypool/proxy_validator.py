import time
from dataclasses import dataclass

from utils.log import log
from utils.parser import WebParser


@dataclass(frozen=True)
class ProxyStatus:
    proxy: str
    health: float
    is_valid: bool


@log
class ProxyValidator:
    def __init__(self, test_url, healthcheck, timeout=10, checks=3):
        self.test_url = test_url
        self.checks = checks
        self.timeout = timeout
        self.healthcheck = healthcheck
        self.web_parser = WebParser()

    def validate(self, proxy_record):
        self.logger.info(f"Proxy Status:")
        consecutive_checks = []
        for _ in range(self.checks):
            content = self.web_parser.get_content(self.test_url, self.timeout, proxies=proxy_record.proxy)
            time.sleep(0.1)
            consecutive_checks.append(int(content is not None))

        health = sum(consecutive_checks) / self.checks

        proxy_status = ProxyStatus(
            proxy=proxy_record.proxy,
            health=health,
            is_valid=health > self.healthcheck
        )

        self.logger.info(f"Proxy Status: {proxy_status}")

        return proxy_status
