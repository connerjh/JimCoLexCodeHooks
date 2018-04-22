#!/usr/bin/env bash

zip -r JimCoLexCodeHooks.zip pymysql balance_inquiry.py jimco.py lambda_function.py \
    purchase.py utilities.py rds_config.py

aws lambda update-function-code \
--region us-east-1 \
--function-name   JimCoLexCodeHooks  \
--zip-file fileb://JimCoLexCodeHooks.zip
