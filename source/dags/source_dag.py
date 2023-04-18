from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from operators.proxy_pool_operator import ProxyPoolOperator
from utils.constants import CRAWLER_CONFIG_PATH


def dummy_callable(action):
    return f"{datetime.now()}: {action} scrapping feeds!"


def create_dag(dag_id, interval):
    with DAG(
            dag_id=dag_id,
            description=f"Scrape latest feeds",
            schedule_interval=interval,
            start_date=datetime(2020, 1, 1),
            catchup=False,
            is_paused_upon_creation=False
    ) as dag:
        start = PythonOperator(
            task_id="start pipeline",
            python_callable=dummy_callable,
            op_kwargs={"action": "starting"},
            dag=dag
        )

        proxypool = ProxyPoolOperator(
            task_id="update proxypool",
            config_path=CRAWLER_CONFIG_PATH,
            dag=dag
        )

        finish = PythonOperator(
            task_id="finish pipeline",
            python_callable=dummy_callable,
            op_kwargs={"action": "finishing"},
            dag=dag
        )

        # events = [
        #     export_events(config, rss_feed, language, dag)
        #     for rss_feed in rss_feeds
        # ]
        #
        # finish = PythonOperator(
        #     task_id="finishing_pipeline",
        #     python_callable=dummy_callable,
        #     op_kwargs={"action": "finishing"},
        #     dag=dag
        # )

        start >> proxypool >> finish

    return dag


n = 4
interval = f"{n * 4}-59/10 * * * *"
create_dag(1, interval)
