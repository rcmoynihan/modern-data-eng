import base64
from pydantic import BaseModel
import redis
from typing import Any, Dict


class KinesisStreamDataModel(BaseModel):
    product_name: str
    was_purchased: bool


def process_record(record: Dict[str, Any], redis_client: redis.Redis):
    """
    Process a record from a Kinesis stream and update the product price in Redis.

    Args:
        record (Dict[str, Any]): The record data from the Kinesis stream.
        redis_client (redis.Redis): The Redis client used to interact with Redis.

    Returns:
        None
    """
    # Decode the base64-encoded data
    encoded_data = record['kinesis']['data']
    decoded_data = base64.b64decode(encoded_data).decode('utf-8')

    # Deserialize and validate the record data
    data = KinesisStreamDataModel.model_validate_json(decoded_data)

    # Redis key for the product price
    redis_key = f"{data.product_name}_price"

    # Increment or decrement the price
    if data.was_purchased:
        redis_client.incrbyfloat(redis_key, 0.05)
    else:
        redis_client.incrbyfloat(redis_key, -0.05)


def lambda_handler(event, context):
    """
    Lambda function handler for processing records from a Kinesis stream.

    Args:
        event (dict): The event data passed to the Lambda function.
        context (object): The context object passed to the Lambda function.

    Returns:
        None
    """

    # Connect to Redis (replace with your Redis configuration)
    redis_client = redis.Redis(host="redis", port=6379, db=0)

    # Process each record in the Kinesis stream
    for record in event["Records"]:
        process_record(record, redis_client)