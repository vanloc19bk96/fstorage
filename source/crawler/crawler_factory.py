import source.plugins.crawler as module_crawler
from utils.constants import SERVICE_KEY, OBJECT_TYPE_KEY, OBJECT_ARGUMENTS_KEY


class CrawlerFactory: 
    def get_crawlers(self, config):
        crawler_services = list(config[SERVICE_KEY].keys())
        crawlers = []
        for crawler_service in crawler_services:
            object_type = config[SERVICE_KEY][crawler_service][OBJECT_TYPE_KEY]
            object_args = config[SERVICE_KEY][crawler_service][OBJECT_ARGUMENTS_KEY]
            crawler = config.init_object(object_type, object_args, module_crawler)
            crawlers.append(crawler)

        return crawlers