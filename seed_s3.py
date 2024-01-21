import json
import aioboto3
import asyncio
from faker import Faker
import random
from typing import List, Dict
import os
from io import BytesIO

# Configuration for LocalStack
os.environ['AWS_ACCESS_KEY_ID'] = 'test'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

# Endpoint for localstack S3
s3_endpoint_url = 'http://localhost:4566'  # Update this with your LocalStack endpoint if different

def generate_pageview_data(num_records: int) -> List[Dict]:
    """
    Generate mock pageview data for an e-commerce site.

    Args:
    num_records (int): Number of records to generate.

    Returns:
    List[Dict]: A list of dictionaries, each representing a pageview.
    """
    fake = Faker()
    pageviews = []

    absurd_product_names = {
        "Unicorn Tears": 1,
        "Invisible Toaster": 2,
        "Glow-in-the-Dark Socks": 3,
        "Banana Umbrella": 4,
        "Toothpaste Flavored Ice Cream": 5,
        "Flying Carpet": 6,
        "Bubble Wrap Suit": 7,
        "Singing Fish Slippers": 8,
        "Pizza-Flavored Toothpaste": 9,
        "Rainbow-Colored Bacon": 10
    }

    for _ in range(num_records):
        pageview = {
            "id": fake.uuid4(),
            "user_id": fake.uuid4(),
            "product_name": random.choices(population=list(absurd_product_names.keys()), weights=list(absurd_product_names.values()))[0],
            "timestamp": fake.iso8601(),
            "session_length_ms": fake.random_int(min=1000, max=100000),
            "referrer": fake.url(),
            "ip_address": fake.ipv4(),
            "user_agent": fake.user_agent()
        }
        pageviews.append(pageview)

    return pageviews

async def upload_file(session, bucket_name: str, key: str, record: Dict):
    """
    Asynchronously upload a single file to S3.

    Args:
    session: The aioboto3 session.
    bucket_name (str): Name of the S3 bucket.
    key (str): S3 object key.
    record (Dict): The record to upload.
    """
    async with session.client('s3', endpoint_url=s3_endpoint_url) as s3:
        try:
            data = BytesIO(json.dumps(record).encode())
            await s3.upload_fileobj(data, bucket_name, key)
            print(f"Uploaded {key} to {bucket_name}.")
        except Exception as e:
            print(f"Unable to upload {key} to {bucket_name}: {e} ({type(e)})")

async def upload_to_s3(bucket_name: str, data: List[Dict], partition_date: str):
    """
    Asynchronously upload generated data to an S3 bucket, partitioned by a specific date.

    Args:
    bucket_name (str): Name of the S3 bucket.
    data (List[Dict]): Data to upload.
    partition_date (str): Date to use for partitioning in 'yyyy/mm/dd' format.
    """
    partition_path = f"year={partition_date.split('/')[0]}/month={partition_date.split('/')[1]}/day={partition_date.split('/')[2]}/"
    session = aioboto3.Session()

    upload_tasks = []
    for i, record in enumerate(data):
        key = partition_path + f"pageview_{i}.json"
        task = asyncio.ensure_future(upload_file(session, bucket_name, key, record))
        upload_tasks.append(task)

    await asyncio.gather(*upload_tasks)

async def main():
    bucket_name = 'raw'  # Name of the S3 bucket
    num_records = 100   # Number of pageview records to generate
    partition_date = '2024/01/01'  # Partition date

    # Generate mock pageview data
    pageviews = generate_pageview_data(num_records)

    # Upload data to S3
    await upload_to_s3(bucket_name, pageviews, partition_date)

if __name__ == "__main__":
    asyncio.run(main())
