from airflow.models import Variable
from airflow.decorators.python import python_task
import urllib.request
import os

@python_task(task_id='downloading_data', multiple_outputs=True)
def download_dataset():
    dataset = Variable.get("avocado_dag_dataset_settings", deserialize_json=True)
    output = dataset['filepath'] + dataset['filename']
    urllib.request.urlretrieve(dataset['url'], filename=output)
    return {"filename": dataset['filename'], "filesize": os.path.getsize(output)}

@python_task(task_id='sanity_check')
def check_dataset(filesize):
    if (filesize <= 0):
        raise ValueError('Dataset is empty')

def read_rmse():
    accuracy = 0
    with open('/tmp/out-model-avocado-prediction-rmse.txt') as f:
        accuracy = float(f.readline())
    return 'accurate' if accuracy < 0.15 else 'inaccurate'