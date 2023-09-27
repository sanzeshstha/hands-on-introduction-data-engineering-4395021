'''ETL task'''
from datetime import datetime,date
import pandas as pd
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow import DAG

with DAG(
    dag_id='ETL_dag',
    description='This DAG transforms the overall ETL task',
    schedule=None,
    catchup=False,
    start_date=datetime(2023,9,27)
    ) as dag:

    extract = BashOperator(
                        task_id='extract',
                        bash_command='wget https://datahub.io/core/top-level-domain-names/r/top-level-domain-names.csv.csv -O /workspaces/hands-on-introduction-data-engineering-4395021/lab/end-to-end/airflow-data-extract.csv',
                        dag=dag)

    def transform_data():
        '''Reada the extracted file and write in the transformed file'''
        today = date.today()
        df = pd.read_csv("/workspaces/hands-on-introduction-data-engineering-4395021/lab/end-to-end/airflow-data-extract.csv")
        generic_type_df = df[df['Type']=='generic']
        generic_type_df.loc[:,"Date"] = today.strftime('%Y-%m-%d')
        generic_type_df.to_csv("/workspaces/hands-on-introduction-data-engineering-4395021/lab/end-to-end/airflow-data-transformed.csv",index=False)

    transform = PythonOperator(
        task_id = 'transform_task',
        python_callable=transform_data,
        dag=dag)

    load = BashOperator(
        task_id='load_task',
        bash_command='echo -e ". separator ","\n.import --skip 1 /workspaces/hands-on-introduction-data-engineering-4395021/lab/end-to-end/airflow-data-transformed.csv top_level_domains" | sqlite3 /workspaces/hands-on-introduction-data-engineering-4395021/lab/end-to-end/basic-etl-load-db.db',
        dag = dag
        )

    extract >> transform >> load
