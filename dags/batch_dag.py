from datetime import datetime, timedelta
import json
from airflow import DAG
from airflow.providers.amazon.aws.operators.lambda_function import (
    LambdaInvokeFunctionOperator,
)
from airflow.providers.amazon.aws.operators.s3 import S3CopyObjectOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.email import EmailOperator
from airflow.models import Variable

from util.s3 import find_latest_partition
from util.notify import generate_failure_email_operator


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=30),
}

# Define a DAG (Directed Acyclic Graph) for the ETL process. This sets up the entire workflow.
dag = DAG(
    "page_views_etl",
    default_args=default_args,
    description="Perform ETL on S3 data and transfer to ClickHouse",
    schedule_interval=timedelta(days=1),
)

# BranchPythonOperator to decide which partition of data to process.
# It uses a Python function to determine the latest partition.
get_partition = BranchPythonOperator(
    task_id="get_latest_partition",
    python_callable=find_latest_partition,
    op_kwargs={"bucket_name": "raw"},
    dag=dag,
)

# Extract the latest partition key from an Airflow Variable.
partition = Variable.get("latest_partition_key")

# Format the date from the partition key.
date_fmt = datetime.strptime(partition, "year=%Y/month=%m/day=%d").strftime("%Y-%m-%d")

# Define keys for aggregated and validated data.
aggregated_key = f"aggregated/{date_fmt}.csv"
validated_key = f"validated/{date_fmt}.csv"

# An operator to signify the end of the DAG run.
notify_end_run_no_data = EmailOperator(
    task_id="notify_end_run_no_data",
    to="data_eng_team@rainforest.com",
    subject=f"Airflow alert: No data found for {date_fmt}",
    html_content=f"<h3>No data found for {date_fmt}</h3>",
    dag=dag,
)

# LambdaInvokeFunctionOperator to call a Lambda function for aggregating data.
aggregate_data = LambdaInvokeFunctionOperator(
    task_id="aggregate_data",
    function_name="BatchTransform",
    payload=json.dumps({"latest_partition_key": partition, "aggregated_key": aggregated_key}),
    aws_conn_id="aws_localstack",
    dag=dag,
)

# LambdaInvokeFunctionOperator to call a Lambda function for validating data.
validate_data = LambdaInvokeFunctionOperator(
    task_id="validate_data",
    function_name="Validate",
    payload=json.dumps({"aggregated_key": aggregated_key}).encode("utf-8"),
    aws_conn_id="aws_localstack",
    dag=dag,
)

# Operator to copy data from one S3 bucket to another after validation, preparing it for ClickHouse.
load_clickhouse = S3CopyObjectOperator(
    task_id="load_clickhouse",
    source_bucket_key=aggregated_key,
    dest_bucket_key=validated_key,
    source_bucket_name="staging",
    dest_bucket_name="clickhouse",
    aws_conn_id="aws_localstack",
    dag=dag,
)

# Set up email operators for task failures
aggregate_data_failure_email = generate_failure_email_operator("aggregate_data", dag)
validate_data_failure_email = generate_failure_email_operator("validate_data", dag)
load_clickhouse_failure_email = generate_failure_email_operator("load_clickhouse", dag)

# Define the workflow sequence: Get partition, then aggregate data, validate, and load to ClickHouse.
get_partition >> [aggregate_data, notify_end_run_no_data]
aggregate_data >> validate_data >> load_clickhouse

# Set dependencies for email alerts on failure
aggregate_data >> aggregate_data_failure_email
validate_data >> validate_data_failure_email
load_clickhouse >> load_clickhouse_failure_email