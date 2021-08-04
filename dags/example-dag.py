from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.decorators.python import python_task

from datetime import datetime

default_args = {
    'start_date': datetime(2020, 1, 1)
}

@python_task
def extract():
    return 50

@python_task
def process(filesize):
    if (filesize >= 50):
        print("well done")

with DAG('example_dag', schedule_interval='@daily', default_args=default_args, catchup=False) as dag:

    downloading_dataset = extract()
    waiting_data = DummyOperator(task_id="waiting_data")
    sanity_check = process(downloading_dataset)

    downloading_dataset >> waiting_data >> sanity_check