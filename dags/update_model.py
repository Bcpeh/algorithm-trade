from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from src.update_model import update_model  # Assuming update_model is defined in a separate Python file

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'update_tsla_model',
    default_args=default_args,
    description='Update TSLA model daily',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 4, 1),  # Replace with your desired start date
    catchup=False,
)

update_model_task = PythonOperator(
    task_id='update_model',
    python_callable=update_model,
    dag=dag,
)

