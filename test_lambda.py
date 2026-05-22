import pytest
import boto3
import json
from handler import lambda_handler

ENDPOINT_URL = "http://localhost:4566"
REGION = "us-east-1"

@pytest.fixture(scope="module")
def setup_dynamodb():
    dynamodb = boto3.resource('dynamodb', endpoint_url=ENDPOINT_URL, region_name=REGION)
    try:
        table = dynamodb.create_table(
            TableName='mahasiswa',
            KeySchema=[{'AttributeName': 'StudentId', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'StudentId', 'AttributeType': 'S'}],
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        table.meta.client.get_waiter('table_exists').wait(TableName='mahasiswa')
    except Exception:
        table = dynamodb.Table('mahasiswa')
        
    table.put_item(Item={'StudentId': '24360002', 'Nama': 'Putri'})
    table.put_item(Item={'StudentId': '24360002', 'Nama': 'Joko'})
    yield table
    table.delete()

def test_get_students_lambda(setup_dynamodb):
    response = lambda_handler({}, {})
    assert response['statusCode'] == 200
    body_data = json.loads(response['body'])
    assert len(body_data) > 0
    print("Test Sukses!")
