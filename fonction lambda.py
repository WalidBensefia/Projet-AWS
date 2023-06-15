import json
import os
from slack_sdk.webhook import WebhookClient

"""
Load environment variables (channel and webhook)
"""
SLACK_WEBHOOK_URL = os.environ["SLACK_WEBHOOK_URL"]
SLACK_CHANNEL = os.environ["SLACK_CHANNEL"]


webhook = WebhookClient(SLACK_WEBHOOK_URL)
"""
Send a message to Slack
"""


def send_slack_message(**kwargs):
    # Build notification ui
    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": "*GuardDuty Finding*"}},
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Account ID:*\n{kwargs.get('account_id')}",
                },
                {"type": "mrkdwn", "text": f"*Region:*\n{kwargs.get('region')}"},
                {
                    "type": "mrkdwn",
                    "text": f"*Finding Type:*\n{kwargs.get('finding_type')}",
                },
                {"type": "mrkdwn", "text": f"*User Type:*\n{kwargs.get('user_type')}"},
                {"type": "mrkdwn", "text": f"*User Name:*\n{kwargs.get('user_name')}"},
                {
                    "type": "mrkdwn",
                    "text": f"*Description:*\n{kwargs.get('description')}",
                },
                {"type": "mrkdwn", "text": f"*Severity:*\n{kwargs.get('severity')}"},
            ],
        },
    ]
    # Send notification
    webhook.send(blocks=blocks)


"""
Your main function should be added under the lambda_handler function
"""


def lambda_handler(event, context):
    #Extract necessary information from the event
    message = event["Records"][0]["Sns"]["Message"]
    message = json.loads(message)
    finding = message["detail"]

    kwargs = {
        "account_id": finding["accountId"],
        "region": finding["region"],
        "finding_type": finding["type"],
        "user_type": finding["resource"]["accessKeyDetails"]["userType"],
        "user_name": finding["resource"]["accessKeyDetails"]["userName"],
        "description": finding["description"],
        "severity": finding["severity"],
    }

    # Send the message to Slack
    send_slack_message(**kwargs)
    return {"statusCode": 200, "body": "message sent !"}
