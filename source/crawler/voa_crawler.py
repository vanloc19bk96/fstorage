from base_crawler import BaseCrawler

class VOACrawler(BaseCrawler):
    def __init__(self, url):
        super().__init__(url)

    def extract(self):
        return super().crawl()