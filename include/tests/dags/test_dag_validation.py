import pytest
from airflow.models import DagBag

@pytest.fixture(scope="class")
def dagbag():
    return DagBag()

class TestDagValidation():

    def test_number_of_dags(self, dagbag):
        stats = dagbag.dagbag_stats
        dag_num = sum([o.dag_num for o in stats])
        assert dag_num == 3, "Wrong number of DAGs"


