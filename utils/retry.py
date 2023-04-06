import functools

from utils.log import log


@log
class RetryOnException:
    def __init__(self, retries):
        self.retries = retries

    def __call__(self, function):
        functools.update_wrapper(self, function)

        def wrapper(*args, **kwargs):
            self.logger.info(f"Retries: {self.retries}")
            while self.retries != 0:
                try:
                    return function(*args, **kwargs)
                except Exception as err:
                    self.logger.info(f"Error occurred: {err}")
                    self.retries -= 1
                    self.raise_on_condition(self.retries, err)

        return wrapper

    def raise_on_condition(self, retries, exception):
        if retries == 0:
            raise exception
        else:
            self.logger.info(f"Retries: {retries}")
