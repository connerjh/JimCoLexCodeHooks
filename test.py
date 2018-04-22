import lambda_function

event1 = {
  "currentIntent": {
    "slots": {
      "AccountNumber": 12345,
      "LastFourSSN": 1111
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

event2 = {
  "currentIntent": {
    "slots": {
      "AccountNumber": 12345,
      "LastFourSSN": 2345,
      "Amount": 100.0
    },
    "name": "Purchase",
    "confirmationStatus": "None"
  },
  "bot": {
    "alias": "$LATEST",
    "version": "$LATEST",
    "name": "JimCoCientServicing"
  },
  "userId": "John",
  "invocationSource": "FulfillmentCodeHook",
  "outputDialogMode": "Text",
  "messageVersion": "1.0",
  "sessionAttributes": {
    "Account": "{\"IndividualId\": 1, \"FirstName\": \"Bob\", \"LastName\": \"Smith\", \"UserName\": \"bob\", \"LastFourSSN\": 1111, \"AccountNumber\": 12345, \"AccountValue\": 10.0, \"AccountId\": 1, \"SocialCode\": 1}",
    "IdentityConfirmed": True
  }
}

context = None

print(lambda_function.lambda_handler(event1, context))
