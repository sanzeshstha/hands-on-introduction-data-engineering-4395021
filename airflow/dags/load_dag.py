'''Load DAG'''
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow import DAG

with DAG(
    dag_id='load_DAG',
    start_date=datetime(2023,9,27),
    schedule_interval=None,
    catchup=False
) as dag:
    load_job = BashOperator(
        task_id='load_task',
        bash_command='echo -e ". separator ","\n.import --skip 1 /workspaces/hands-on-introduction-data-engineering-4395021/lab/orchestrated/airflow-data-transformed.csv top_level_domains" | sqlite3 /workspaces/hands-on-introduction-data-engineering-4395021/lab/orchestrated/airflow-load-db.db',
        dag = dag
    )
