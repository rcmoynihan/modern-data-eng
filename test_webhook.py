from flask import Flask, request
import smtplib
from email.message import EmailMessage
from typing import Any, Dict

app = Flask(__name__)


def send_email(subject: str, body: str, recipient: str) -> None:
    """
    Sends an email to the specified recipient using a local Maildev server.

    Args:
    subject (str): The subject of the email.
    body (str): The body of the email.
    recipient (str): The recipient's email address.
    """
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = "webhook@signoz.example"
    msg["To"] = recipient

    # Configure these settings for your local Maildev server
    smtp_server = "localhost"
    smtp_port = 1025

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.send_message(msg)


@app.route("/webhook", methods=["POST"])
def webhook() -> Any:
    """
    Webhook endpoint to receive data from SigNoz and send an email.

    Returns:
    Any: A response to the webhook request.
    """
    print("sending email")
    return "", 200
    data: Dict[str, Any] = request.json
    # Here you can extract and format the data from SigNoz as needed
    # For simplicity, we'll just send a basic email

    subject = "SigNoz Alert"
    body = f"Alert from SigNoz: {data}"
    recipient = "recipient@example.com"

    send_email(subject, body, recipient)

    return "Email sent", 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
