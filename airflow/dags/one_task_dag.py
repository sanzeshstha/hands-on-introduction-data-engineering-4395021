'''One task DAG'''
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow import DAG

default_args = {
    'owner': 'Clark Kent',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 0,
    'catchup': False,
    'start_date': datetime(2023,9,23)
}

with DAG(
    dag_id='one_task_dag',
    description='A one task Airflow DAG',
    schedule=None,
    default_args=default_args
    ) as dag:

    task1 = BashOperator(
                        task_id='one_task',
                        bash_command='echo "Hello, this is a course exerice" > /workspaces/hands-on-introduction-data-engineering-4395021/lab/temp/test.txt',
                        dag=dag)
