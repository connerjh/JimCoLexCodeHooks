import jimcodb
import utilities
import logging
import json

# -----------------------------------------------------------------------------

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# -----------------------------------------------------------------------------

def handle_balance_inquiry(intent_request):
    logger.info('Handling balance inquiry')

    invocation_source = intent_request['invocationSource']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    slots = intent_request['currentIntent']['slots']

    if 'Account' in session_attributes:
        account = json.loads(session_attributes['Account'])
    else:
        account = None

    if invocation_source == 'DialogCodeHook':

        if 'AccountNumber' in slots and slots['AccountNumber'] is not None and 'Account' not in session_attributes:

            account_number = slots['AccountNumber']

            logger.info('Validating Account Number')

            account = jimcodb.get_account(account_number)

            if account is not None:
                session_attributes['Account'] = json.dumps(account)

            else:
                slots['AccountNumber'] = None
                return utilities.elicit_slot(
                    session_attributes,
                    intent_request['currentIntent']['name'],
                    slots,
                    'AccountNumber',
                    'The account number <say-as interpret-as="digits">{}</say-as> cannot be found. Can you provide another number?'.format(account_number)
                )

        elif 'LastFourSSN' in slots and slots['LastFourSSN'] is not None and account is not None:

            logger.info('Validating LastFourSSN')

            if int(slots['LastFourSSN']) == account['LastFourSSN']:
                session_attributes['IdentityConfirmed'] = True

            else:
                last_4_ssn = int(slots['LastFourSSN'])
                slots['LastFourSSN'] = None
                return utilities.elicit_slot(
                    session_attributes,
                    intent_request['currentIntent']['name'],
                    slots,
                    'LastFourSSN',
                    'The last four digits, <say-as interpret-as="digits">{}</say-as>, you have provided do not match the account <say-as interpret-as="digits">{}</say-as>. Can provide another four digits?'.format(last_4_ssn,
                                                                                                                                       account['AccountNumber'])
                )

    elif invocation_source == 'FulfillmentCodeHook':

        if account is not None and 'IdentityConfirmed' in session_attributes:
            # def close(session_attributes, fulfillment_state, message):

            messages = jimcodb.get_account_messages(account['AccountNumber'])

            balance_message = 'The account value for account <say-as interpret-as="digits">{}</say-as> is ${} .'.format(account['AccountNumber'], account['AccountValue'])

            if messages and len(messages) > 0:

                response = utilities.confirm_intent(
                    session_attributes,
                    "AgentAssistance",
                    {"PhoneNumber": None},
                    balance_message + " " + messages[0]['AccountMessage'] + ", May I transfer you to an associate?"
                )

            else:

                session_attributes.pop('Account')

                response = utilities.close(
                    session_attributes,
                    'Fulfilled',
                    'The account value for account <say-as interpret-as="digits">{}</say-as> is ${} .'.format(account['AccountNumber'], account['AccountValue'])
                )

            return response

    return utilities.delegate(session_attributes, slots)

