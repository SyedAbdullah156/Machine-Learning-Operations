from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def start_number():
    print("Hello I am Start Number")

def multiply_five():
    print("Hello I multiply by Five")

myDag = DAG(
    "mypipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@daily"
)

task1 = PythonOperator(
    task_id="task1",
    python_callable=start_number,
    dag=myDag
)

task2 = PythonOperator(
    task_id="task2",
    python_callable=multiply_five,
    dag=myDag   
)

task1 >> task2