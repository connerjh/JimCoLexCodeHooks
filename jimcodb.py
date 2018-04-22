import logging
import pymysql
import rds_config
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ------------------------------------------------------------------------------


def get_connection():

    rds_host = rds_config.db_endpoint
    name = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name
    port = rds_config.db_port

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    try:

        return pymysql.connect(rds_host, port=port, user=name, passwd=password, db=db_name, connect_timeout=5)

    except Exception as e:

        logger.error("ERROR: Unexpected error: Could not connect to MySql instance. {}".format(e))

    logger.info("SUCCESS: Connection to RDS mysql instance succeeded")

# ------------------------------------------------------------------------------


def set_account_value(account):

    try:

        connection = get_connection()

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "UPDATE jimcodb.Accounts as a SET a.AccountValue = %s where a.AccountId = %s;",
                (
                    account['AccountValue'],
                    account['AccountId']
                )
            )

        logger.info('Account {} updated with value {}'.format(account['AccountId'], account['AccountValue']))

        connection.commit()

        return account

    except Exception as e:

        logger.error('JimCoAccountQuery Error: ' + str(e))
        return None


# -----------------------------------------------------------------------------


def get_account(account_number):

    try:

        connection = get_connection()

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM jimcodb.IndividualAccountView where AccountNumber = %s;", (account_number,))
            account = cursor.fetchone()
            logger.info('returned account: {}'.format(json.dumps(account)))
            return account

    except Exception as e:

        logger.error('JimCoAccountQuery Error: ' + str(e))
        return None
