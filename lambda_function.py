import asyncio
import json
import logging
import boto3
import aioboto3
from datetime import datetime
from typing import Dict
from collections import defaultdict
from contextlib import closing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

AWS_CREDENTIALS = {
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test"
}
AWS_ENDPOINT_URL = 'http://localhost:4566'

def lambda_handler(event, context):
    try:
        # Find the latest partition
        latest_partition_key = find_latest_partition('raw')
        if not latest_partition_key:
            logger.warning("No partitions found in the bucket.")
            return {'status': 'No data'}

        # Extract base path for the latest partition
        base_path = '/'.join(latest_partition_key.split('/')[:-1])

        # Run the asynchronous process_partition function
        aggregated_data = asyncio.run(process_partition('raw', base_path))

        # Write the output file to the staging bucket
        write_to_s3(aggregated_data, base_path)

        return {'status': 'Success'}

    except Exception as e:
        logger.error(f"Error in processing: {e}")
        return {'status': 'Error', 'message': str(e)}

def find_latest_partition(bucket_name: str) -> str:
    """
    Find the latest partition in the S3 bucket.

    :param bucket_name: The name of the S3 bucket.
    :return: The key of the latest partition.
    """
    with closing(boto3.client('s3', endpoint_url=AWS_ENDPOINT_URL, **AWS_CREDENTIALS)) as s3_client:
        try:
            paginator = s3_client.get_paginator('list_objects_v2')
            result = paginator.paginate(Bucket=bucket_name, Prefix='year=')
            
            latest_date = None
            latest_partition = None

            for page in result:
                if "Contents" in page:
                    for obj in page['Contents']:
                        key = obj['Key']
                        date_str = "/".join(key.split('/')[1:3])  # Assuming the format 'year=YYYY/month=MM/day=DD/...'
                        current_date = datetime.strptime(date_str, 'month=%m/day=%d')
                        if not latest_date or current_date > latest_date:
                            latest_date = current_date
                            latest_partition = key

            logger.info(f"Latest partition: {latest_partition.split('/')[:-1]}")
            return latest_partition

        except Exception as e:
            logger.error(f"Error finding latest partition in {bucket_name}: {e}")
            return None

async def process_file(bucket_name: str, key: str, aggregated_data: Dict, s3_client: aioboto3.Session.client):
    """
    Process a single file asynchronously and update the aggregated data.

    :param bucket_name: The name of the S3 bucket.
    :param key: The key of the file in the S3 bucket.
    :param aggregated_data: The dict to store the aggregated data.
    """
    response = await s3_client.get_object(Bucket=bucket_name, Key=key)
    file_content = await response['Body'].read()
    data = json.loads(file_content.decode('utf-8'))

    product_name = data['product_name']
    session_length = data['session_length_ms']
    aggregated_data[product_name] += session_length

async def process_partition(bucket_name: str, partition_path: str) -> Dict:
    """
    Process all files within a partition asynchronously and aggregate session lengths.

    :param bucket_name: The name of the S3 bucket.
    :param partition_path: The base path for the partition.
    :return: A dict containing the aggregated session lengths.
    """
    aggregated_data = defaultdict(int)

    async with aioboto3.Session().client('s3', endpoint_url=AWS_ENDPOINT_URL, **AWS_CREDENTIALS) as s3_client:
        paginator = s3_client.get_paginator('list_objects_v2')
        result = paginator.paginate(Bucket=bucket_name, Prefix=partition_path)
        
        tasks = []
        async for page in result:
            if "Contents" in page:
                for obj in page['Contents']:
                    key = obj['Key']
                    # Create a coroutine for each file and add it to the list of tasks
                    tasks.append(process_file(bucket_name, key, aggregated_data, s3_client))

        # Wait for all file processing tasks to complete
        await asyncio.gather(*tasks)

    return aggregated_data

def write_to_s3(data: Dict, original_key: str):
    """
    Write the aggregated data to the staging S3 bucket.

    :param data: The aggregated data dict.
    :param original_key: The original S3 key of the input file.
    """
    try:
        staging_bucket = 'staging'
        # Extract the date from the original key and format it for the new key
        date = datetime.strptime(original_key, 'year=%Y/month=%m/day=%d').strftime('%Y-%m-%d')
        new_key = f'aggregated/{date}.json'

        # Convert data to JSON
        json_data = json.dumps(data)

        # Write to S3
        with closing(boto3.client('s3', endpoint_url=AWS_ENDPOINT_URL, **AWS_CREDENTIALS)) as s3_client:
            s3_client.put_object(Bucket=staging_bucket, Key=new_key, Body=json_data)
            logger.info(f"Successfully wrote aggregated data to {staging_bucket}/{new_key}")

    except Exception as e:
        logger.error(f"Error writing data to {staging_bucket}: {e}")
        raise



# This is for testing the lambda function locally.
if __name__ == "__main__":
    lambda_handler(None, None)
