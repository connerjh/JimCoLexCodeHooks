import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def confirm_intent(session_attributes, intent_name, slots, message, message_type="PlainText"):
    response = {
        'sessionAttributes': session_attributes,
        "dialogAction": {
            "type": "ConfirmIntent",
            "slots": slots,
            "message": {
                "contentType": message_type,
                "content": message
            },
            "intentName": intent_name,
        }
    }

    logger.info("Confirm intent response: {}".format(response))

    return response


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message, message_type="PlainText"):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': {'contentType': message_type, 'content': message}
        }
    }

    logger.info("Elicit response: {}".format(response))

    return response


def close(session_attributes, fulfillment_state, message, message_type="PlainText"):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': {'contentType': message_type, 'content': message}
        }
    }

    logger.info("Close response: {}".format(response))

    return response


def delegate(session_attributes, slots):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }

    logger.info("Delegate response: {}".format(response))

    return response
