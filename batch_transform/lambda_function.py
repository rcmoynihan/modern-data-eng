import asyncio
import json
import logging
import boto3
import aioboto3
from typing import Any, Dict
from collections import defaultdict
from contextlib import closing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

AWS_CREDENTIALS = {
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test",
    "endpoint_url": "http://localstack:4566",
    "region_name": "us-east-1",
}


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        logger.info(f"Received event: {event}")

        # Find the latest partition
        latest_partition_key = event.get("latest_partition_key")
        if not latest_partition_key:
            logger.warning("No partitions found in the bucket.")
            return {"status": "No data"}

        # Run the asynchronous process_partition function
        aggregated_data = asyncio.run(process_partition("raw", latest_partition_key))

        # Write the output file to the staging bucket
        aggregated_key = event.get("aggregated_key")
        write_to_s3(aggregated_data, aggregated_key)

        return {"status": "Success"}

    except Exception as e:
        logger.error(f"Error in processing: {e}")
        return {"status": "Error", "message": str(e), "event": event}


async def process_file(
    bucket_name: str,
    key: str,
    aggregated_data: Dict,
    s3_client: aioboto3.Session.client,
):
    """
    Process a single file asynchronously and update the aggregated data.

    :param bucket_name: The name of the S3 bucket.
    :param key: The key of the file in the S3 bucket.
    :param aggregated_data: The dict to store the aggregated data.
    """
    response = await s3_client.get_object(Bucket=bucket_name, Key=key)
    file_content = await response["Body"].read()
    data = json.loads(file_content.decode("utf-8"))

    product_name = data["product_name"]
    session_length = data["session_length_ms"]
    was_purchased = data["was_purchased"]

    aggregated_data[product_name]["total_session_view_time_ms"] += session_length
    aggregated_data[product_name]["total_sessions"] += 1
    aggregated_data[product_name]["total_purchases"] += 1 if was_purchased else 0


async def process_partition(bucket_name: str, partition_path: str) -> Dict:
    """
    Process all files within a partition asynchronously and aggregate session lengths.

    :param bucket_name: The name of the S3 bucket.
    :param partition_path: The base path for the partition.
    :return: A dict containing the aggregated session lengths.
    """
    aggregated_data = defaultdict(lambda: defaultdict(int))

    async with aioboto3.Session().client("s3", **AWS_CREDENTIALS) as s3_client:
        paginator = s3_client.get_paginator("list_objects_v2")
        result = paginator.paginate(Bucket=bucket_name, Prefix=partition_path)

        tasks = []
        async for page in result:
            if "Contents" in page:
                for obj in page["Contents"]:
                    key = obj["Key"]
                    # Create a coroutine for each file and add it to the list of tasks
                    tasks.append(
                        process_file(bucket_name, key, aggregated_data, s3_client)
                    )

        # Wait for all file processing tasks to complete
        await asyncio.gather(*tasks)

    return aggregated_data


def write_to_s3(data: Dict, aggregated_key: str):
    """
    Write the aggregated data to the staging S3 bucket.

    :param data: The aggregated data dict.
    :param original_key: The original S3 key of the input file.
    """
    try:
        staging_bucket = "staging"

        # Convert data to JSON
        json_data = json.dumps(data)

        # Write to S3
        with closing(boto3.client("s3", **AWS_CREDENTIALS)) as s3_client:
            s3_client.put_object(
                Bucket=staging_bucket, Key=aggregated_key, Body=json_data
            )
            logger.info(
                f"Successfully wrote aggregated data to {staging_bucket}/{aggregated_key}"
            )

    except Exception as e:
        logger.error(f"Error writing data to {staging_bucket}: {e}")
        raise


# This is for testing the lambda function locally.
if __name__ == "__main__":
    lambda_handler(
        json.dumps(
            {
                "body": {
                    "latest_partition_key": "year=2024/month=01/day=01",
                    "aggregated_key": "aggregated/2024-01-01.json",
                }
            }
        ).encode("utf-8"),
        None,
    )
