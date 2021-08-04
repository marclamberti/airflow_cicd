from airflow.utils.task_group import TaskGroup
from airflow.providers.papermill.operators.papermill import PapermillOperator

def training_group():
    with TaskGroup("trainings", tooltip="Training tasks") as group:
        n_estimators = [100, 150]
        max_features = ['auto', 'sqrt']
        for feature in max_features:
            for estimator in n_estimators:
                ml_id = f"{feature}_{estimator}"
                PapermillOperator(
                    task_id=f'training_model_{ml_id}',
                    input_nb='/usr/local/airflow/include/notebooks/avocado_prediction.ipynb',
                    output_nb=f'/tmp/out-model-avocado-prediction-{ml_id}.ipynb',
                    pool='training_pool',
                    parameters={
                        'filepath': '/tmp/avocado.csv',
                        'n_estimators': estimator,
                        'max_features': feature,
                        'ml_id': ml_id
                    }
                )
    return group