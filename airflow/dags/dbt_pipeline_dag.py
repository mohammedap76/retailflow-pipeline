from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mohammed',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id="retailflow_pipeline",
    description="RetailFlow: Generate and Load data to Snowflake",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False,
    tags=["retailflow", "snowflake"],
) as dag:

    generate_data = BashOperator(
        task_id="generate_data",
        bash_command="""
            cd /opt/airflow && 
            python scripts/generate_data.py
        """,
    )

    load_to_snowflake = BashOperator(
        task_id="load_to_snowflake",
        bash_command="""
            cd /opt/airflow && 
            python scripts/load_to_snowflake.py
        """,
    )

    generate_data >> load_to_snowflake