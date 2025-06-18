from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    "owner": "wilson",
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="donor_pipeline_dag",
    default_args=default_args,
    description="Ingest FEC data, run dbt, refresh dashboard",
    schedule_interval="@daily",
    start_date=days_ago(1),
    catchup=False,
) as dag:

    clean_and_load = BashOperator(
        task_id="clean_and_load_data",
        bash_command="python /opt/airflow/scripts/process_fec_contributions.py"
    )

    run_dbt = BashOperator(
        task_id="run_dbt_models",
        bash_command="cd /opt/airflow/dbt_project && dbt run"
    )

    test_dbt = BashOperator(
        task_id="test_dbt_models",
        bash_command="cd /opt/airflow/dbt_project && dbt test"
    )

    clean_and_load >> run_dbt >> test_dbt
