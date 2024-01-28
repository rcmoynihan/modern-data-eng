import logging
from pydantic import BaseModel, ValidationError
from datetime import datetime
import json
from urllib.parse import unquote
import boto3
from typing import Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the Pydantic model for the uploaded data
class UploadDataModel(BaseModel):
    id: str
    user_id: str
    product_name: str
    timestamp: datetime
    session_length_ms: int
    was_purchased: bool
    referrer: str
    ip_address: str
    user_agent: str


# Define the Pydantic model for the Kinesis message
class KinesisMessageModel(BaseModel):
    product_name: str
    was_purchased: bool


def fetch_file_from_s3(bucket_name: str, object_key: str) -> Any:
    """
    Fetches a file from an S3 bucket.

    Args:
        bucket_name (str): The name of the S3 bucket.
        object_key (str): The key of the object in the S3 bucket.

    Returns:
        Any: The content of the file as a deserialized JSON object.
    """
    # Decoding the URL-encoded object key
    object_key = unquote(object_key)

    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    content = response["Body"].read().decode("utf-8")
    return content


def send_to_kinesis(data: KinesisMessageModel, stream_name: str) -> dict:
    """
    Sends the given data to the specified Kinesis stream.

    Args:
        data (KinesisMessageModel): The data to be sent to Kinesis.
        stream_name (str): The name of the Kinesis stream.

    Returns:
        dict: The response from the Kinesis client.
    """
    kinesis_client = boto3.client("kinesis")
    response = kinesis_client.put_record(
        StreamName=stream_name,
        Data=data.model_dump_json(),
        PartitionKey=data.product_name,
    )
    return response


def lambda_handler(event, context):
    """
    Lambda function handler for processing S3 events.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (object): The runtime information of the Lambda function.

    Returns:
        None

    Raises:
        ValidationError: If data validation fails.

    """
    for record in event["Records"]:
        message_body = json.loads(record["body"])
        s3_info = message_body["Records"][0]["s3"]
        logger.info(f"Processing S3 event for {s3_info['bucket']['name']}/{s3_info['object']['key']}")

        # Fetch the file content from S3
        file_content = fetch_file_from_s3(
            s3_info["bucket"]["name"], s3_info["object"]["key"]
        )

        try:
            # Validate the data using the Pydantic model
            upload_data = UploadDataModel.model_validate_json(file_content)

            # Prepare and send the Kinesis message
            kinesis_data = KinesisMessageModel(
                product_name=upload_data.product_name,
                was_purchased=upload_data.was_purchased,
            )
            response = send_to_kinesis(kinesis_data, "pricing_model_stream")

            print(f"Message sent to Kinesis: {response}")

        except ValidationError as e:
            print(f"Data validation failed: {e}")
            raise e
