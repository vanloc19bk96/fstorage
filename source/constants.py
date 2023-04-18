from enum import Enum

PROXY = "proxy"
URL = "url"
TESTING_URL = "testing_url"
HEALTHCHECK = "healthcheck"
NUMBER_OF_PROXIES = "number_of_proxies"
PROXY_STORAGE_DB = "storage_key"
PROXY_STORAGE = "storage"
NUMBER_OF_WORKERS = "number_of_workers"
LIMIT_PROXIES = "limit"
DAG_CONFIG = "dag_config"
START_DATE = "start_date"
DAY = "day"
MONTH = "month"
YEAR = "day"
DESCRIPTION = "description"
SCHEDULE = "schedule"
CATCHUP = "catchup"
IS_PAUSED_UPON_CREATION = "is_paused_upon_creation"
ACTION = "action"


class TaskID(Enum):
    START_PIPELINE = "start_pipeline"
    FINISH_PIPELINE = "end_pipeline"
    PROXY_POOL = "update_proxypool"
