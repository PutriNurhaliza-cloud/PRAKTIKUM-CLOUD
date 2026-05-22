import json
import boto3
import os

if os.environ.get('LOCALSTACK_HOSTNAME'):
    endpoint_url = f"http://{os.environ['LOCALSTACK_HOSTNAME']}:4566"
    dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url, region_name='us-east-1')
else:
    dynamodb = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:4566", region_name='us-east-1')

table = dynamodb.Table('mahasiswa')

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response.get('Items', [])
        return { 'statusCode': 200, 'body': json.dumps(items) }
    except Exception as e:
        return { 'statusCode': 500, 'body': json.dumps({'error': str(e)}) }