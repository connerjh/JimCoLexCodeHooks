import jimcodb
import utilities
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# -----------------------------------------------------------------------------

def handle_purchase(intent_request):
    logger.info('Handling purchase')

    invocation_source = intent_request['invocationSource']
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    slots = intent_request['currentIntent']['slots']

    if 'Account' in session_attributes:
        account = json.loads(session_attributes['Account'])
    else:
        account = None

    if 'BotOrigin' in session_attributes and 'JimCoConnect' == session_attributes['BotOrigin']:
        use_SSML = True
    else:
        use_SSML = False

    if invocation_source == 'DialogCodeHook':

        if 'AccountNumber' in slots and slots['AccountNumber'] is not None and 'Account' not in session_attributes:

            account_number = slots['AccountNumber']

            logger.info('Validating Account Number')

            account = jimcodb.get_account(account_number)

            if account is not None:
                session_attributes['Account'] = json.dumps(account)
                return utilities.delegate(session_attributes, slots)

            else:

                if use_SSML:
                    message_type = "SSML"
                    message = '<speak>The account number  <say-as interpret-as="digits">{}</say-as> cannot be found. Can you provide another number?</speak>'.\
                        format(account_number)
                else:
                    message_type = "PlainText"
                    message = 'The account number {} cannot be found. Can you provide another number?'.\
                        format(account_number)

                slots['AccountNumber'] = None
                return utilities.elicit_slot(
                    session_attributes,
                    intent_request['currentIntent']['name'],
                    slots,
                    'AccountNumber',
                    message,
                    message_type
                )

        elif 'LastFourSSN' in slots and slots['LastFourSSN'] is not None and account is not None and 'IdentityConfirmed' not in session_attributes:

            logger.info('Validating LastFourSSN')

            if int(slots['LastFourSSN']) == account['LastFourSSN']:
                session_attributes['IdentityConfirmed'] = True
                return utilities.delegate(session_attributes, slots)

            else:
                last_4_ssn = int(slots['LastFourSSN'])
                slots['LastFourSSN'] = None
                if use_SSML:
                    message_type = "SSML"
                    message = '<speak>The last four digits, <say-as interpret-as="digits">{}</say-as>, you have provided do not match the account <say-as interpret-as="digits">{}</say-as>. Can provide another four digits?</speak>'.\
                        format(last_4_ssn, account['AccountNumber'])
                else:
                    message_type = "PlainText"
                    message = 'The last four digits, {}, you have provided do not match the account {}. Can provide another four digits?'.\
                        format(last_4_ssn, account['AccountNumber'])

                return utilities.elicit_slot(
                    session_attributes,
                    intent_request['currentIntent']['name'],
                    slots,
                    'LastFourSSN',
                    message,
                    message_type
                )

        elif 'Amount' in slots and slots['Amount'] is not None and account is not None:

            logger.info('Validating Amount {}'.format(slots['Amount']))

            session_attributes['IdentityConfirmed'] = True

            if str(slots['Amount']).isdigit():
                return utilities.delegate(session_attributes, slots)
            else:
                amount = slots['Amount']
                slots['Amount'] = None

                return utilities.elicit_slot(
                    session_attributes,
                    intent_request['currentIntent']['name'],
                    slots,
                    'Amount',
                    'The amount, {}, you have provided is not a valid amount. Can you confirm the amount?'.format(amount)
                )

    elif invocation_source == 'FulfillmentCodeHook':

        amount = float(slots['Amount'])

        if account is not None and 'IdentityConfirmed' in session_attributes:

            account['AccountValue'] = account['AccountValue'] + amount

            logger.info('Fullfilling Purchase with amount {}'.format(amount))

            account = jimcodb.set_account_value(account)

            session_attributes.pop('Account')

            logger.info('updated account: {}'.format(account))

            if use_SSML:
                message_type = "SSML"
                message = '<speak>We have successfully invested ${} into the account <say-as interpret-as="digits">{}</say-as>. Your new balance is ${}</speak>'.format(
                    amount,
                    account['AccountNumber'],
                    account['AccountValue']
                )
            else:
                message_type = "PlainText"
                message = 'We have successfully invested ${} into the account {}. Your new balance is ${}'.format(
                    amount,
                    account['AccountNumber'],
                    account['AccountValue']
                )

            return utilities.close(
                session_attributes,
                'Fulfilled',
                message,
                message_type
            )

        else:

            return utilities.close(
                session_attributes,
                'Failed',
                'We have failed to process your request'
            )

    return utilities.delegate(session_attributes, slots)

