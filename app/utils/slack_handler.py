"""
This file contain functions to help interact
with slack related tasks
"""
import os
import requests


def _send_slack_message(title, content, color='good'):
    """ Sends a slack notification

    Args:
        title: str Title of the notification
        content: str Content of the notification
        color: str Color of the notification

    Returns:
        str: Response status code if no errors in the Slack Request,
        else returns the Exception error
    """
    slack_webhook = os.getenv('SLACK_WEBHOOK')  # Get slack Webhook from env

    attachment = {'title': title, 'text': content, 'color': color}
    message = {'attachments': [attachment]}

    try:
        response = requests.post(slack_webhook, json=message)
        return str(response.status_code)
    except Exception as error:
        return str(error)


def create_product_update_notification(product):
    """Create a message to be sent with the product information

    :param product: Product updated

    :return: send_slack_message response
    """
    title = f'Product {product.sku} updated'
    content = f'New product information:\n' \
              f'- *Name:* {product.name}\n' \
              f'- *Price:* {product.price}\n' \
              f'- *Brand:* {product.brand}\n'

    return _send_slack_message(title, content)
