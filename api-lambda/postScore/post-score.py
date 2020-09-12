import boto3
import uuid
import json
import logging
import decimal
import os
import datetime
from botocore.exceptions import ClientError
# パッチ適用
from aws_xray_sdk.core import patch
patch(['boto3'])

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb',region_name = 'ap-northeast-1')
table = dynamodb.Table(os.getenv('TABLE_NAME'))

def generate_id():
    return str(uuid.uuid4())

def lambda_handler(event, context):
    logger.info(event)
    text = json.dumps(event['body'])
    item2 = json.loads(text, parse_float=decimal.Decimal)
    try:
        table.put_item(
            Item = item2
        )
    except ClientError as e:
        logging.info(e.response['Error']['Message'])
        response = {
            'statusCode': '400',
            'body': e.response['Error']['Message'],
            'headers': {
                'Content-Type': 'application/json'
            },
        }
        return response
    else:
        response = {
            'statusCode': '200',
            'body': json.dumps(event['body']),
            'headers': {
                'Content-Type': 'application/json'
            },
        }
    return response