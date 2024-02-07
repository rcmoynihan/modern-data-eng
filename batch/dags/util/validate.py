import os
import tempfile
from great_expectations.data_context import DataContext
import boto3
from contextlib import closing


AWS_CREDENTIALS = {
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test",
    "endpoint_url": "http://localstack:4566",
    "region_name": "us-east-1",
}


def gx_validate(data_context: DataContext, checkpoint_name: str, s3_key: str) -> str:
    """
    Validates the data using the specified checkpoint in the given data context.

    Args:
        data_context (DataContext): The data context containing the checkpoint.
        checkpoint_name (str): The name of the checkpoint to run.
        s3_key (str): The key of the CSV file in the S3 bucket.

    Returns:
        str: The name of the next step to execute based on the validation result.
            - If the validation is successful, returns "load_clickhouse".
            - If the validation fails, returns "notify_validation_did_not_pass".
    """
    directory = "/opt/airflow/dags/include/data/"

    if not os.path.exists(directory):
        os.makedirs(directory)

    with tempfile.NamedTemporaryFile(
        dir=directory, suffix=".csv", delete=True
    ) as tmp_file:
        fetch_csv_from_s3(s3_key, tmp_file.name)

        # Create a batch request for the temporary file
        data_asset = data_context.get_datasource("aggregated_data").get_asset(
            "aggregated_data_asset"
        )
        batch_request = data_asset.build_batch_request()

        # Run the checkpoint using the data context
        result = data_context.run_checkpoint(
            checkpoint_name, batch_request=batch_request
        )

    if result["success"]:
        return "copy_to_clickhouse_s3"
    else:
        return "notify_validation_did_not_pass"


def fetch_csv_from_s3(key: str, local_path: str) -> None:
    """
    Fetches a CSV file from S3 and returns it as a Pandas DataFrame.

    Args:
        key (str): The key of the CSV file in the S3 bucket.
        local_path (str): The path to save the CSV file to.
    """
    with closing(boto3.client("s3", **AWS_CREDENTIALS)) as s3:
        obj = s3.get_object(Bucket="staging", Key=key)

        # Read the content of the object
        with open(local_path, "wb") as file:
            file.write(obj["Body"].read())
