import boto3
import json
from typing import Dict, Any
from great_expectations.data_context import DataContext
from great_expectations.dataset import PandasDataset

def validate_data(data: Dict[str, Any], context: DataContext, expectation_suite_name: str) -> Dict[str, Any]:
    """
    Validate the given data using Great Expectations.

    Args:
    data (Dict[str, Any]): The data to validate.
    context (DataContext): The Great Expectations DataContext.
    expectation_suite_name (str): The name of the expectation suite to use for validation.

    Returns:
    Dict[str, Any]: The validation results.
    """
    # Convert data to Pandas DataFrame
    df = pd.DataFrame.from_dict(data, orient='index')
    
    # Load the expectation suite
    suite = context.get_expectation_suite(expectation_suite_name)
    
    # Create a Great Expectations dataset
    dataset = PandasDataset(df, expectation_suite=suite)
    
    # Validate the data
    results = dataset.validate()
    return results.to_json_dict()

def lambda_handler(event: Dict[str, Any], context: Any) -> None:
    """
    AWS Lambda function handler to validate aggregated product data.

    Args:
    event (Dict[str, Any]): The event triggering the lambda function.
    context (Any): The context in which the lambda function is running.
    """
    s3_client = boto3.client('s3')
    bucket_name = "staging"
    aggregated_key = event["aggregated_key"]

    # Fetch the data from S3
    response = s3_client.get_object(Bucket=bucket_name, Key=aggregated_key)
    data = json.load(response['Body'])

    # Setup Great Expectations context
    ge_context = DataContext("/path/to/great_expectations")

    # Validate data
    validation_results = validate_data(data, ge_context, "your_expectation_suite_name")
    print(validation_results)