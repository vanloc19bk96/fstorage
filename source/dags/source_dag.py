from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from operators.proxy_pool_operator import ProxyPoolOperator
from utils.constants import CRAWLER_CONFIG_PATH
from source.constants import START_DATE, DAY, MONTH, YEAR, DESCRIPTION, SCHEDULE, CATCHUP, \
    IS_PAUSED_UPON_CREATION, ACTION, DAG_CONFIG, TaskID
from utils.parser import ConfigParser


def dummy_callable(action):
    return f"{datetime.now()}: {action}"


def get_start_date(config):
    day = int(config[DAG_CONFIG][START_DATE][DAY])
    month = int(config[DAG_CONFIG][START_DATE][MONTH])
    year = int(config[DAG_CONFIG][START_DATE][YEAR])
    start_date = datetime(year, month, day)

    return start_date


def create_dag(dag_id, config):
    start_date = get_start_date(config)
    dag_description = config[DAG_CONFIG][DESCRIPTION]
    schedule = str(config[DAG_CONFIG][SCHEDULE])
    catchup = config[DAG_CONFIG][CATCHUP]
    is_paused_upon_creation = config[DAG_CONFIG][IS_PAUSED_UPON_CREATION]

    with DAG(
            dag_id=str(dag_id),
            description=dag_description,
            schedule_interval=schedule,
            start_date=start_date,
            catchup=catchup,
            is_paused_upon_creation=is_paused_upon_creation
    ) as dag:
        start = PythonOperator(
            task_id=TaskID.START_PIPELINE.value,
            python_callable=dummy_callable,
            op_kwargs={ACTION: TaskID.START_PIPELINE.value},
            dag=dag
        )

        proxypool = ProxyPoolOperator(
            task_id=TaskID.PROXY_POOL.value,
            config=config,
            dag=dag
        )

        finish = PythonOperator(
            task_id=TaskID.FINISH_PIPELINE.value,
            python_callable=dummy_callable,
            op_kwargs={ACTION: TaskID.FINISH_PIPELINE.value},
            dag=dag
        )

        # events = [
        #     export_events(config, rss_feed, language, dag)
        #     for rss_feed in rss_feeds
        # ]

        start >> proxypool >> finish

    return dag


config = ConfigParser.from_args(CRAWLER_CONFIG_PATH)
globals()['1'] = create_dag(1, config)
# dag.test()
