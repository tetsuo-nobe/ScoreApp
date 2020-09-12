import boto3
import uuid
import json
import logging
import os
import datetime
import decimal
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key, Attr
# パッチ適用
from aws_xray_sdk.core import patch
patch(['boto3'])

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
table = dynamodb.Table(os.getenv('TABLE_NAME'))

def lambda_handler(event, context):
        logging.info(event)
        try:
            response = table.query(
                KeyConditionExpression=Key('userid').eq(event['userid'])
            )
            #response = table.scan(
            #    FilterExpression=Attr('userid').eq(event['userid']))
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
            items = json.dumps(response['Items'], cls=DecimalEncoder)
            response = {
                'statusCode': '200',
                'body': items,
                'headers': {
                    'Content-Type': 'application/json'
                },
            }
        return response
