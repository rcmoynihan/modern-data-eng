from datetime import datetime
import boto3
from contextlib import closing
import logging
from airflow.models import Variable


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

AWS_CREDENTIALS = {
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test"
}
AWS_ENDPOINT_URL = 'http://localstack:4566'


def find_latest_partition(bucket_name: str) -> str:
    """
    Find the latest partition in the S3 bucket.

    In a real production environment, you would check to see if the latest partition has already been processed.

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
                            latest_partition = "/".join(key.split('/')[:-1])

            logger.info(f"Latest partition: {latest_partition}")

            Variable.set("latest_partition_key", latest_partition)
            return "aggregate_data"

        except Exception as e:
            logger.error(f"Error finding latest partition in {bucket_name}: {e}")
            return "notify_end_run_no_data"

if __name__ == "__main__":
    find_latest_partition('raw')