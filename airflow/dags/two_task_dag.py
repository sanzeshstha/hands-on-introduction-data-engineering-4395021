'''Two task DAG'''
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
    dag_id='two_task_dag',
    description='A two task Airflow DAG',
    schedule=None,
    default_args=default_args
    ) as dag:

    task1 = BashOperator(
                        task_id='bash_task_1',
                        bash_command='echo "First Airflow Task"'
                        )
    task2 = BashOperator(
        task_id='bash_task_2',
        bash_command='date "+%Y-%m-%d %H:%M"'

    )

    task1 >> task2
