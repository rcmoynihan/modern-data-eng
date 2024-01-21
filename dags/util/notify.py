from airflow import DAG
from airflow.utils.trigger_rule import TriggerRule
from airflow.operators.email import EmailOperator

def generate_failure_email_operator(task_id: str, dag: DAG) -> EmailOperator:
    """
    Generates an EmailOperator for the given task.

    Args:
    task_id (str): The ID of the task for which the email will be sent upon failure.
    dag (DAG): The DAG to which the EmailOperator belongs.

    Returns:
    EmailOperator: An instance of EmailOperator configured to send an email on failure.
    """
    return EmailOperator(
        task_id=f"{task_id}_failure_email",
        to="data_eng_team@rainforest.com",
        subject=f"Airflow alert: {task_id} Failed",
        html_content=f"<h3>{task_id} failed.</h3>",
        dag=dag,
        trigger_rule=TriggerRule.ONE_FAILED
    )
