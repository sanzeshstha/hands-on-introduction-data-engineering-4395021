'''Transformation DAG'''
from datetime import datetime, date
import pandas as pd
from airflow.operators.python import PythonOperator
from airflow import DAG


with DAG(
    dag_id='transform_DAG',
    description='This DAG transforms the extracted data using pandas library',
    schedule=None,
    catchup=False,
    start_date=datetime(2023,9,24)
    ) as dag:

    def transform_data():
        '''Read the extracted file and write in the transformed file'''
        today = date.today()
        df = pd.read_csv("/workspaces/hands-on-introduction-data-engineering-4395021/lab/orchestrated/airflow-data-extract.csv")
        generic_type_df = df[df['Type']=='generic']
        generic_type_df.loc[:,"Date"] = today.strftime('%Y-%m-%d')
        generic_type_df.to_csv("/workspaces/hands-on-introduction-data-engineering-4395021/lab/orchestrated/airflow-data-transformed.csv",index=False)

    transform = PythonOperator(
        task_id = 'transform_task',
        python_callable=transform_data,
        dag=dag)
