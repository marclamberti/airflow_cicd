from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.dummy import DummyOperator
from airflow.sensors.filesystem import FileSensor
from include.helpers.astro import download_dataset, read_rmse, check_dataset
from airflow.utils.edgemodifier import Label
from airflow.models.baseoperator import chain, cross_downstream
from airflow.operators.sql import BranchSQLOperator
from plugins.notebook_plugin.operators.notebook_to_keep_operator import NotebookToKeepOperator
from plugins.notebook_plugin.operators.notebook_to_git_operator import NotebookToGitOperator

from datetime import timedelta, datetime
from include.groups.training_group import training_group

default_args = {
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_failure': False,
    'email_on_retry': False,
    'start_date': datetime(2020, 1, 1)
}

with DAG('avocado_dag', description='Forecasting avocado prices', 
    schedule_interval='*/10 * * * *', default_args=default_args, 
    catchup=False) as dag:

    creating_accuracy_table = PostgresOperator(
        task_id='creating_accuracy_table',
        sql='sql/CREATE_TABLE_ACCURACIES.sql',
        postgres_conn_id='postgres'
    )

    downloading_data = download_dataset()

    waiting_for_data = FileSensor(
        task_id='waiting_for_data',
        fs_conn_id='fs_default',
        filepath='avocado.csv',
        poke_interval=15,
        mode='poke',
    )

    sanity_check = check_dataset(downloading_data['filesize'])

    training_model_tasks = training_group()

    evaluating_rmse = BranchSQLOperator(
        task_id='evaluating_rmse',
        sql='sql/FETCH_MIN_RMSE.sql',
        conn_id='postgres',
        follow_task_ids_if_true='accurate',
        follow_task_ids_if_false='inaccurate'
    )

    accurate = DummyOperator(task_id='accurate')

    fetch_best_model = NotebookToKeepOperator(
        task_id='fetch_best_model',
        sql='sql/FETCH_BEST_MODEL.sql',
        postgres_conn_id='postgres'
    )

    publish_notebook = NotebookToGitOperator(
        task_id='publish_notebook',
        conn_id='git',
        nb_path='/tmp',
        nb_name='out-model-avocado-prediction-{{ ti.xcom_pull(task_ids="fetch_best_model") }}.ipynb'
    )

    inaccurate = DummyOperator(task_id='inaccurate')

    label_accurate = Label("RMSE < 0.15")
    label_inaccurate = Label("RMSE >= 0.15")

    creating_accuracy_table >> downloading_data >> waiting_for_data >> sanity_check >> training_model_tasks >> evaluating_rmse
    evaluating_rmse >> label_accurate >> accurate >> fetch_best_model >> publish_notebook
    evaluating_rmse >> label_inaccurate >> inaccurate





	