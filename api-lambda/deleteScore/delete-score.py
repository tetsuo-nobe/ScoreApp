import boto3
import uuid
import json
import logging
import os
import datetime
import decimal
from botocore.exceptions import ClientError
# パッチ適用
from aws_xray_sdk.core import patch
patch(['boto3'])

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb', region_name='ap-northeast-1')
table = dynamodb.Table(os.getenv('TABLE_NAME'))


def lambda_handler(event, context):
    try:
        userid    = event['userid']
        startdate = event['startdate']
        try:
            response = table.get_item(
              Key={
                'userid': userid,
                'startdate': startdate
              }
            )

            if 'Item' not in response:
              logging.info("Specified key is not found.")
              response = {
                  'statusCode': '404',
                  'body': 'Not Found',
                  'headers': {
                      'Content-Type': 'application/json'
                  },
              }
              return response
            else:
                logging.info("Delete start." + userid + ":" +startdate)
                response = table.delete_item(
                    Key={
                        'userid': userid,
                        'startdate': startdate
                    }
                )

        except ClientError as e:
            logging.info(e.response['Error']['Message'])
            response = {
                'statusCode': '400',
                'body': e.response['Error']['Message'],
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
            return response
        else:
            logging.info(
                'Item (userid = ' + userid + ',startdate =  ' + startdate +  ') is sucessfully deleted')
            response = {
                'statusCode': '204',
                'body': '',
                'headers': {
                    'Content-Type': 'application/json'
                }
            }
            return response
    except Exception as e:
        logging.error("type : %s", type(e))
        logging.error(e)
