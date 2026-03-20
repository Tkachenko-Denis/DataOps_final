from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator


def extract():
    print("Extract step completed")


def transform():
    print("Transform step completed")


def load():
    print("Load step completed")


with DAG(
    dag_id="demo_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["demo", "final-project"],
) as dag:
    extract_task = PythonOperator(task_id="extract", python_callable=extract)
    transform_task = PythonOperator(task_id="transform", python_callable=transform)
    load_task = PythonOperator(task_id="load", python_callable=load)

    extract_task >> transform_task >> load_task
