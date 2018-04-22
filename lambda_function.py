import logging
import balance_inquiry
import purchase
import agent_assistance
import utilities

logger = logging.getLogger()
logger.setLevel(logging.INFO)


# -----------------------------------------------------------------------------

def dispatch(intent_request):
    logger.info('intent request: {}'.format(intent_request))

    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'BalanceInquiry':
        return balance_inquiry.handle_balance_inquiry(intent_request)
    elif intent_name == 'Purchase':
        return purchase.handle_purchase(intent_request)
    elif intent_name == 'AgentAssistance':
        return agent_assistance.handle_agent_assistance(intent_request)
    else:
        slots = intent_request['currentIntent']['slots']
        output_session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
        return utilities.delegate(output_session_attributes, slots)


# ------------------------------------------------------------------------------


def lambda_handler(event, context):
    return dispatch(event)
