from dataclasses import dataclass, field

from bs4 import BeautifulSoup
from source.crawler.base_crawler import BaseCrawler
from utils.log import log
from utils.parser import WebParser


@dataclass
class ProxyRecord:
    ip_address: str
    port: int
    code: str
    country: str
    anonymity: str
    google: str
    https: str
    last_checked: str
    proxy: dict = field(init=False, default=None)

    def __post_init__(self):
        self.proxy = self.format_proxy()

    def format_proxy(self):
        protocol = "https" if self.https == "yes" else "http"
        url = f"{protocol}://{self.ip_address}:{self.port}"
        return {"http": url, "https": url}


@log
class ProxyCrawler(BaseCrawler):
    def __init__(self, url, bs_parser="html.parser"):
        self.web_parser = WebParser()
        self.bs_parser = bs_parser
        super().__init__(url)

    def extract(self):
        content = self.web_parser.get_content(self.url)
        soup_object = BeautifulSoup(content, self.bs_parser)

        return (
            soup_object
            .find(id="list")
            .find_all("tr")
        )

    def get_proxy_stream(self, number_of_proxies):
        proxy_records = self.extract()
        clean_records = list(map(self.clear_records, proxy_records))

        for record in clean_records[:number_of_proxies]:
            self.logger.info(f"Proxy record: {record}")
            if record:
                yield ProxyRecord(*record)

    def clear_records(self, raw_record):
        return [
            val.text for val
            in raw_record.find_all("td")
        ]
