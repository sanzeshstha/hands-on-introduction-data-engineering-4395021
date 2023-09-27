'''ETL task'''
from datetime import datetime,date
import pandas as pd
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

with DAG(
    dag_id='Challenge_ETL_dag',
    description='This DAG transforms the overall ETL task',
    schedule=None,
    catchup=False,
    start_date=datetime(2023,9,27)
    ) as dag:

    extract = BashOperator(
                        task_id='extract',
                        bash_command='wget https://datahub.io/core/s-and-p-500-companies/r/constituents.csv -O /workspaces/hands-on-introduction-data-engineering-4395021/lab/challenge/airflow-data-extract.csv',
                        dag=dag)

    def transform_data():
        '''Read the extracted data and transform/wrangle the data'''
        df = pd.read_csv("/workspaces/hands-on-introduction-data-engineering-4395021/lab/challenge/airflow-data-extract.csv")
        today = date.today()
        agg_df = df.groupby('Sector',sort=False).agg({'Name': 'count'})
        agg_df.loc[:,"Date"] = today.strftime('%Y-%m-%d')
        agg_df.to_csv("/workspaces/hands-on-introduction-data-engineering-4395021/lab/challenge/airflow-data-transform.csv")

    transform = PythonOperator(
        task_id = 'Calling_python_task_to_transform',
        python_callable=transform_data,
        dag=dag
    )

    load = BashOperator(
        task_id = 'load_task',
        bash_command='sqlite3 /workspaces/hands-on-introduction-data-engineering-4395021/lab/challenge/challenge-load-db.db ".mode csv" ".import --skip 1 /workspaces/hands-on-introduction-data-engineering-4395021/lab/challenge/airflow-data-transform.csv sp_500_sector_count"',
        dag=dag
    )

    extract >> transform >> load
