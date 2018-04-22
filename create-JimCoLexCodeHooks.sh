#!/usr/bin/env bash

zip -r JimCoLexCodeHooks.zip pymysql balance_inquiry.py jimco.py lambda_function.py \
    purchase.py utilities.py rds_config.py

aws lambda create-function \
--region us-east-1 \
--function-name   JimCoLexCodeHooks  \
--zip-file fileb://JimCoLexCodeHooks.zip \
--role arn:aws:iam::832433821903:role/JimCoLamdaExecution \
--handler JimCoLexCodeHooks.lambda_handler \
--runtime python3.6 \
--vpc-config SubnetIds=[],SecurityGroupIds=[]
