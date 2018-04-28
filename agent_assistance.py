import utilities
import logging
import json
import boto3
import base64

# -----------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# -----------------------------------------------------------------------------


def handle_agent_assistance(intent_request):

    logger.info('Handling agent assistance')

    invocation_source = intent_request['invocationSource']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    slots = intent_request['currentIntent']['slots']

    if 'Account' in session_attributes:
        account = json.loads(session_attributes['Account'])
    else:
        account = None

    logger.info('Account {}:'.format(account))

    if invocation_source == 'DialogCodeHook':

        if 'BotOrigin' in session_attributes and 'JimCoConnect' == session_attributes['BotOrigin']:

            logger.info('setting phone number to blank.')
            slots['PhoneNumber'] = "+10000000000"

            return utilities.close(session_attributes, "Fulfilled", 'One moment while we connect you.')

        else:

            return utilities.delegate(session_attributes, slots)

    elif invocation_source == 'FulfillmentCodeHook':

        if 'BotOrigin' in session_attributes and 'JimCoConnect' == session_attributes['BotOrigin']:

            logger.info('Routing to an agent.')

            return utilities.close(session_attributes, "Fulfilled", 'One moment while we connect you.')

        else:

            client = boto3.client("lambda")

            payload = json.dumps({
                "DestinationPhoneNumber": slots['PhoneNumber'],
                "Attributes": {
                    'Name': account["FirstName"] + " " + account["LastName"],
                    'AccountNumber': str(account['AccountNumber'])
                }
            })

            logger.info('payload: {}'.format(payload))

            response = client.invoke(
                FunctionName='OutboundCall',
                InvocationType='RequestResponse',
                LogType='Tail',
                Payload=payload
            )

            logger.info('log: {}'.format(base64.b64decode(response['LogResult'])))

            logger.info('OutboundCall response: {}'.format(response))

            return utilities.close(session_attributes, "Fulfilled", 'We will be calling you shortly')

    return utilities.delegate(session_attributes, slots)

