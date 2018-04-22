import boto3
import logging
import decimal

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def create_update_query(account):
    query = {
        "Table": "JimCoAccounts",
        "Key": {
            "AccountNumber": account['AccountNumber'],
        },
        "UpdateExpression": "SET AccountValue = :val",
        "ExpressionAttributeValues": {
            ":val": account['AccountValue']
        },
        "ReturnValues": "UPDATED_NEW"
    }

    return query


# -----------------------------------------------------------------------------

def set_account(account):
    dynamodb = boto3.resource('dynamodb')
    accounts = dynamodb.Table('JimCoAccounts')

    try:

        logger.info('Update for Account {}'.format(str(account)))
        response = accounts.update_item(
            TableName='JimCoAccounts',
            Key={'AccountNumber': decimal.Decimal(str(account['AccountNumber']))},
            UpdateExpression="set AccountValue = :av",
            ExpressionAttributeValues={
                ':av': decimal.Decimal(str(account['AccountValue'])),
            },
            ReturnValues="UPDATED_NEW"
        )

    except Exception as e:

        logger.error('JimCoAccountQuery Error: {}'.format(str(e)))

    else:

        logger.info('DynamoDB Response: {}'.format(response))

        if 'Attributes' in response:
            return account
        else:
            return None


# -----------------------------------------------------------------------------

def get_account(account_number):
    dynamodb = boto3.resource('dynamodb')
    accounts = dynamodb.Table('JimCoAccounts')

    try:

        logger.info('Query for Account Number {}'.format(account_number))
        response = accounts.get_item(Key={'AccountNumber': int(account_number)})

    except Exception as e:

        logger.error('JimCoAccountQuery Error: ' + str(e))

    else:

        logger.info('DynamoDB Response: {}'.format(response))

        if 'Item' in response:
            account = response['Item']
            account['AccountNumber'] = int(account['AccountNumber'])
            account['LastFourSSN'] = int(account['LastFourSSN'])
            account['AccountValue'] = float(account['AccountValue'])
            logger.info('Account: {}'.format(account))
            return account
        else:
            return None
