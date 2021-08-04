from airflow.exceptions import AirflowException
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.decorators import apply_defaults

class NotebookToKeepOperator(PostgresOperator):

    @apply_defaults
    def __init__(self, *args, **kwargs):
        super(NotebookToKeepOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        self.log.info('Executing: %s', self.sql)
        self.hook = PostgresHook(postgres_conn_id=self.postgres_conn_id, schema=self.database)
        result = self.hook.get_first(self.sql, parameters=self.parameters)
        if not result:
            raise AirflowException("The query returned None")
        record = result[0]
        self.log.info('First record: {0}'.format(record))
        for output in self.hook.conn.notices:
            self.log.info(output)
        return record