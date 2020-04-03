import datetime
import os

import boto3

DB = boto3.client('dynamodb')
TABLE = os.environ['DYNAMODB_TABLE']
DEFAULT_HOST_ID = os.environ['DEFAULT_HOST_ID']
DEFAULT_HOST_NAME = os.environ['DEFAULT_HOST_NAME']


def get_next_tech_chat_date():
    """Get date for next tech chat (will return today if today is Friday)."""
    today = datetime.date.today()
    friday = today + datetime.timedelta((4-today.weekday()) % 7)
    return friday.strftime('%Y%m%d')


def query_host(user_attr):
    """Query for the host, for either the name or user_id."""
    response = DB.get_item(
        TableName=TABLE,
        Key={
            'Date': {'N': '{0}'.format(get_next_tech_chat_date())}
        },
        ProjectionExpression='Host.#attr',
        ExpressionAttributeNames={
            '#attr': user_attr
        }
    )

    if 'Item' not in response:
        update_or_add_host(DEFAULT_HOST_ID, DEFAULT_HOST_NAME)
        host = DEFAULT_HOST_NAME
    else:
        host = response['Item']['Host']['M'][user_attr]['S']
    return host


def update_or_add_host(host_id, host_name):
    """Change the host, or set it if there isn't one."""
    result = DB.update_item(
        TableName=TABLE,
        Key={
            'Date': {'N': '{0}'.format(get_next_tech_chat_date())}
        },
        ExpressionAttributeNames={
            '#HN': 'Host'
        },
        ExpressionAttributeValues={
            ':host_map': {
                'M': {
                    'name': {'S': host_name},
                    'user_id': {'S': host_id}
                }
            },
        },
        UpdateExpression='SET #HN = :host_map',
        ReturnValues='UPDATED_NEW'
    )

    return result


def query_all():
    """Get everything for next tech chat to send to the host."""
    response = DB.get_item(
        TableName=TABLE,
        Key={
            'Date': {'N': '{0}'.format(get_next_tech_chat_date())}
        }
    )

    return response['Item']


def add_goldstar(text):
    """Add a goldstar to the end of the list, or create a new list to add the star."""
    result = DB.update_item(
        TableName=TABLE,
        Key={
            'Date': {'N': '{0}'.format(get_next_tech_chat_date())}
        },
        ExpressionAttributeNames={
            '#GS': 'GoldStars'
        },
        ExpressionAttributeValues={
            ':text': {
                "L": [
                    {'S': text}
                ]
            },
            ':empty_list': {
                "L": []
            }
        },
        UpdateExpression='SET #GS = list_append(if_not_exists(#GS, :empty_list), :text)',
        ReturnValues='UPDATED_NEW'
    )

    return result
