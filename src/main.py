from datetime import datetime
import random
import uuid

import boto3

from dataclasses import dataclass

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource(
    'dynamodb',
    endpoint_url='http://localhost:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

existent_tables = []
table_name = 'Products'


table = dynamodb.Table(table_name)


@dataclass
class PriceHistory:
    date: datetime
    price: int


@dataclass
class Product:
    uid: uuid
    price_history: list[PriceHistory]


def list_tables():
    for table in dynamodb.tables.all():
        existent_tables.append(table.name)
        print(table.name)


def create_table():
    if table_name not in existent_tables:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'created_at',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'created_at',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        print(f"✅ Table '{table_name}' created!")


def insert_item(product_to_add: Product):
    table.put_item(
        Item={
            'id': str(product_to_add.uid),
            'created_at': str(datetime.now()),
            'price_history': [
                {
                    'date': str(i.date),
                    'price': i.price
                }
                for i in product_to_add.price_history
            ]
        }
    )


def get_all_items():
    response = table.scan()
    items = response.get('Items', [])
    return items


def get_by_id(uid: uuid):
    response = table.query(
        KeyConditionExpression=Key('id').eq(str(uid))
    )

    item = response.get('Items', None)

    return item[0]


def delete_by_id(uid: str, created_at: str):
    response = table.delete_item(
        Key={
            'id': str(uid),  # PK
            'created_at': created_at  # SK
        }
    )

    return response


if __name__ == '__main__':
    list_tables()
    create_table()

    random_number = random.randint(1, 1000)
    prices = [random_number, random_number, random_number]
    product = Product(
        uid=uuid.uuid4(),
        price_history=[
            PriceHistory(
                date=datetime.now(),
                price=item
            )
            for item in prices
        ]
    )

    insert_item(product_to_add=product)

    products = get_all_items()
    print(products)

    product_id = products[0]['id']

    product = get_by_id(product_id)
    print(product)

    created_at = products[0]['created_at']
    deleted_product = delete_by_id(uid=product_id, created_at=created_at)
    print(deleted_product)
