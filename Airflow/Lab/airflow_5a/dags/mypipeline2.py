from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# ML task with Random Forest
def machine_learning_task(**kwargs):
    ti = kwargs['ti']
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import load_iris

    # Load Iris dataset
    iris = load_iris()
    X = iris.data
    y = iris.target

    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = model.score(X_test, y_test)
    print("Accuracy:", accuracy)

    # Push accuracy to XCom
    ti.xcom_push(key="model_accuracy", value=accuracy)

# Task to print accuracy from XCom
def print_acc(**kwargs):
    ti = kwargs['ti']
    accuracy = ti.xcom_pull(task_ids='python_ML', key='model_accuracy')
    print("Pulled accuracy from XCom:", accuracy)

# DAG definition
with DAG(
    dag_id="machine_learning_rf_dag",
    description="A DAG executing Random Forest ML task",
    start_date=datetime(2023, 7, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    task_bash = BashOperator(
        task_id="bash_task",
        bash_command='echo "Executing bash script..."'
    )

    task_python = PythonOperator(
        task_id="python_ML",
        python_callable=machine_learning_task
    )

    task_print = PythonOperator(
        task_id="print_acc",
        python_callable=print_acc
    )

    # Task dependencies
    task_bash >> task_python >> task_print
