import json
import logging

# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Simple AWS Lambda function that returns "Hello World" and logs an info message.

    :param event: The event object that triggered the function.
    :param context: The runtime information of the function.
    :return: A dictionary with a message.
    """
    # Log an informational message
    logger.info("Hello World function executed successfully")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello World')
    }
