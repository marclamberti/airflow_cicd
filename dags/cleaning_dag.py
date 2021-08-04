import airflow.utils.dates
from airflow import DAG
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

default_args = {
        "owner": "airflow", 
        "start_date": datetime(2020, 1, 1)
    }

with DAG(dag_id="cleaning_dag", 
    default_args=default_args, 
    schedule_interval="*/10 * * * *", catchup=False) as dag:

    waiting_for_task = ExternalTaskSensor(
        task_id='waiting_for_task',
        external_dag_id='avocado_dag',
        external_task_id='publish_notebook',
        failed_states=['failed']
    )

    cleaning_xcoms = PostgresOperator(
        task_id='cleaning_xcoms',
        sql='sql/CLEANING_XCOMS.sql',
        postgres_conn_id='postgres'
    )

    waiting_for_task >> cleaning_xcoms