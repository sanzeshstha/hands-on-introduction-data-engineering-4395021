'''Extract the top level domain file from DataHub.io'''
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow import DAG

with DAG(
    dag_id='extract_top_domain_dag',
    description='This DAG extracts the top level domain from datahub.io',
    schedule=None,
    catchup=False,
    start_date=datetime(2023,9,24)
    ) as dag:

    task1 = BashOperator(
                        task_id='extract',
                        bash_command='wget https://datahub.io/core/top-level-domain-names/r/top-level-domain-names.csv.csv -O /workspaces/hands-on-introduction-data-engineering-4395021/lab/orchestrated/airflow-data-extract.csv',
                        dag=dag)
