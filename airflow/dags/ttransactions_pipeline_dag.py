"""
Airflow DAG: Transactions Pipeline
Runs daily: Ingests CSV, transforms data, and loads into MySQL
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator
from airflow.models import Variable
from datetime import datetime, timedelta
import pandas as pd
import os
from src.transform import validate_and_clean, aggregate_daily_by_bank

# Default args
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# DAG definition
with DAG(
    dag_id="transactions_pipeline",
    default_args=default_args,
    description="Daily banking transactions ETL pipeline",
    schedule_interval="@daily",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["etl", "transactions", "mysql"],
) as dag:

    input_csv = Variable.get("transactions_input_csv", "/opt/airflow/dags/data/sample_transactions.csv")
    target_table = Variable.get("transactions_target_table", "bank_transactions_daily")

    def extract_and_transform(**context):
        df = pd.read_csv(input_csv, parse_dates=["timestamp"])

        # Clean & validate
        df = validate_and_clean(df)

        # Aggregate
        agg_df = aggregate_daily_by_bank(df)

        # Save intermediate file
        out_path = f"/tmp/daily_agg_{context['ds']}.csv"
        agg_df.to_csv(out_path, index=False)
        return out_path

    def load_to_mysql(ti, **context):
        from sqlalchemy import create_engine

        mysql_uri = os.getenv("MYSQL_URI", "mysql+pymysql://root:root@mysql:3306/analytics")
        engine = create_engine(mysql_uri)

        # Pull transformed CSV path from XCom
        out_path = ti.xcom_pull(task_ids="transform_task")
        agg_df = pd.read_csv(out_path)

        agg_df.to_sql(target_table, con=engine, if_exists="append", index=False)

    transform_task = PythonOperator(
        task_id="transform_task",
        python_callable=extract_and_transform,
        provide_context=True,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=load_to_mysql,
        provide_context=True,
    )

    transform_task >> load_task
