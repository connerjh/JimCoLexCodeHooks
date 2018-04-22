import lambda_function

event = {
  "currentIntent": {
    "slots": {
      "AccountNumber": 12345,
      "LastFourSSN": "None"
    },
    "name": "BalanceInquiry",
    "confirmationStatus": "None"
  },
  "bot": {
    "alias": "$LATEST",
    "version": "$LATEST",
    "name": "JimCoCientServicing"
  },
  "userId": "John",
  "invocationSource": "DialogCodeHook",
  "outputDialogMode": "Text",
  "messageVersion": "1.0",
  "sessionAttributes": {}
}

context = None

print(lambda_function.lambda_handler(event, context))