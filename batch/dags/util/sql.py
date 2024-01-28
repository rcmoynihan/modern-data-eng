import re

DATE_PATTERN = r"\d{4}-\d{2}-\d{2}"


def create_table_if_not_exists_query() -> str:
    """
    Returns the SQL query to create a table if it does not already exist.

    Returns:
        str: The SQL query to create the table.
    """
    return """
        create table if not exists product_stats (
            product String,
            total_session_view_time_ms UInt64,
            total_sessions UInt64,
            total_purchases UInt64,
            date Date
        )
        engine = MergeTree
        order by product;
        """


def insert_data_query(s3_path: str) -> str:
    """
    Generates an SQL query to insert data into the product_stats table.

    Args:
        s3_path (str): The S3 path of the data to be inserted.

    Returns:
        str: The SQL query to insert the data.
    """
    return f"""
        insert into product_stats
        select *, toDate('{extract_date(s3_path)}') as date
        from s3('http://localstack:4566/clickhouse/{s3_path}', 'test', 'test', 'CSV', 'product String, total_session_view_time_ms UInt64, total_sessions UInt64, total_purchases UInt64');
        """


def extract_date(s3_path: str) -> str:
    """
    Extracts the date from an S3 path.

    Args:
        s3_path (str): The S3 path from which to extract the date.

    Returns:
        str: The extracted date.

    Raises:
        ValueError: If the date cannot be extracted from the S3 path.
    """
    match = re.search(DATE_PATTERN, s3_path)
    if match:
        return match.group()
    else:
        raise ValueError(f"Could not extract date from {s3_path}")
