from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from functions.ELT import extract, load, transform
from functions.model import data_preparation, model_707

default_args = {
    'owner': 'airflow',
    'retries': 5,
    'retry_delay': timedelta(minutes=10)
}

with DAG(
    dag_id="ETL",
    default_args=default_args, 
    start_date=datetime(2023, 1, 16),
    schedule='@monthly'
) as dag:
    task1 = PythonOperator(
        task_id = 'extract_table',
        python_callable=extract
    )

    task2 = PythonOperator(
        task_id = 'load_table',
        python_callable=load
    )
    
    task3 = PythonOperator(
        task_id = 'transform_table',
        python_callable=transform
    )

    task4 = PythonOperator(
        task_id = 'data_preparation',
        python_callable=data_preparation
    )

    task5 = PythonOperator(
        task_id = 'model_1',
        python_callable=model_707
    )

    task1 >> task2 >> task3 >> task4 >> task5

