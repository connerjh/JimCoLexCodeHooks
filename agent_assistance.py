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

    if invocation_source == 'DialogCodeHook':

        return utilities.delegate(session_attributes, slots)

    elif invocation_source == 'FulfillmentCodeHook':

        pass

        # if account is not None and 'IdentityConfirmed' in session_attributes:
        #
        #     messages = jimcodb.get_account_messages(account['AccountNumber'])
        #
        #     if messages and len(messages) > 0:
        #
        #         response = utilities.confirm_intent(
        #             session_attributes,
        #             "AgentAssistance",
        #             {"PhoneNumber": None},
        #             messages[0]['AccountMessage'] + " May I transfer you to an associate?"
        #         )
        #
        #     else:
        #
        #         session_attributes.pop('Account')
        #
        #         response = utilities.close(
        #             session_attributes,
        #             'Fulfilled',
        #             'The account value for account {} is ${}'.format(account['AccountNumber'], account['AccountValue'])
        #         )
        #
        #     return response

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

