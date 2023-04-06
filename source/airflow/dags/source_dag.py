from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator


def dummy_callable(action, feed_type):
    return f"{datetime.now()}: {action} scrapping RSS feeds!"


def create_dag(dag_id, interval):
    with DAG(
        dag_id=dag_id,
        description=f"Scrape latest ({language}) sport RSS feeds",
        schedule_interval=interval,
        start_date=datetime(2020, 1, 1),
        catchup=False,
        is_paused_upon_creation=False
    ) as dag:

        start = PythonOperator(
            task_id="starting_pipeline",
            python_callable=dummy_callable,
            op_kwargs={"action": "starting"},
            dag=dag
        )

        proxypool = ProxyPoolOperator(
            task_id="updating_proxypoool",
            proxy_webpage=config.PROXY_WEBPAGE,
            number_of_proxies=config.NUMBER_OF_PROXIES,
            testing_url=config.TESTING_URL,
            max_workers=config.NUMBER_OF_PROXIES,
            redis_config=config.REDIS_CONFIG,
            redis_key=config.REDIS_KEY,
            dag=dag
        )

        events = [
            export_events(config, rss_feed, language, dag)
            for rss_feed in rss_feeds
        ]

        finish = PythonOperator(
            task_id="finishing_pipeline",
            python_callable=dummy_callable,
            op_kwargs={"action": "finishing"},
            dag=dag
        )

        start >> proxypool >> events >> finish

    return dag