#!/usr/bin/env bash

git commit -a -m 'commiting'

rm JimCoLexCodeHooks.zip

zip -r JimCoLexCodeHooks.zip pymysql agent_assistance.py balance_inquiry.py jimcodb.py lambda_function.py \
    purchase.py utilities.py rds_config.py

aws lambda update-function-code \
--region us-east-1 \
--function-name   JimCoLexCodeHooks  \
--zip-file fileb://JimCoLexCodeHooks.zip
