from contextlib import closing
from pathlib import Path
from random import random

from httpx import get

from utils.log import log
from utils.util import read_yaml
from utils.constants import HEADERS_LIST
import random


class ConfigParser:
    def __init__(self, config):
        """
            :param config: Content of config file
        """

        self._config = config

    @classmethod
    def from_args(cls, config_path):
        cfg_name = Path(config_path)

        config = read_yaml(cfg_name)

        return cls(config)

    @property
    def config(self):
        return self._config

    def __getitem__(self, name):
        return self.config[name]

    def init_object(self, object_type, object_args, module, *args, **kwargs):
        object_args.update(kwargs)

        return getattr(module, object_type)(*args, **object_args)


@log
class WebParser:
    def random_header(self):
        return random.choice(HEADERS_LIST)

    def get_content(self, url, timeout=30, proxies=None):
        kwargs = {
            "timeout": timeout,
            "proxies": proxies,
            "headers": self.random_header()
        }
        try:
            with closing(get(url, **kwargs)) as response:
                if self.is_good_response(response):
                    return response.content
        except Exception as err:
            self.logger.info(f"Error occurred: {err}")

    def is_good_response(self, response):
        content_type = response.headers['Content-Type'].lower()
        return (
                response.status_code == 200
                and content_type is not None
        )
