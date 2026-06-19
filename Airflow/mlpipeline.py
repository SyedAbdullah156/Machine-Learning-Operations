from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# Define our task 1
def preprocess_data():
    print("Preprocessing data...")
# Define our task task 2
def train_model():
    print("Training model ....")
# Task 3
def evaluate_model():
    print("Evaluate Models ")

# Define DAG
with DAG(
    'ml_pipeline', # NAME OF DAG
    start_date=datetime(2024,1,1),
    schedule='@weekly' # no time pipeline to execute
) as dag:
    # Define the task
    preprocess=PythonOperator(task_id="preprocess_task1",
                              python_callable=preprocess_data)
    train=PythonOperator(task_id="train_task",
                         python_callable=train_model)
    evaluate=PythonOperator(task_id="evaluate_task",
                            python_callable=evaluate_model)
preprocess >> train >> evaluate