from base_crawler import BaseCrawler

class CNNCrawler(BaseCrawler):
    def __init__(self, url):
        super().__init__(url)

    def extract(self):
        return super().crawl()