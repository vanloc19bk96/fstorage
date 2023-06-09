from abc import abstractmethod


class BaseCrawler(object):
    def __init__(self, url):
        self.url = url

    def _get_url(self):
        return self.url

    def set_url(self, url):
        self.url = url

    @abstractmethod
    def extract(self):
        pass
