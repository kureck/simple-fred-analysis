import os
import sys
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text


def db_engine():
    DB_HOST = os.getenv('DB_HOST', None)
    DB_PORT = os.getenv('DB_PORT', None)
    DB_USER = os.getenv('DB_USER', None)
    DB_PASSWD = os.getenv('DB_PASSWD', None)
    DB_NAME = os.getenv('DB_NAME', None)
    connection_url = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWD, DB_HOST, DB_PORT, DB_NAME)
    msg = "Connection URL: {}".format(connection_url)
    logging.debug(msg)
    logging.info("Database engine created.")
    return create_engine(connection_url)


def update(df, table_name, incremental=False):
    engine = db_engine()
    conn = engine.connect()
    if incremental:
        logging.info("Doing incremental update on {}.".format(table_name))
        values = ""
        for value in df.values:
            values += "('{}', '{}'),".format(value[0], value[1])
        values = values.strip(",")
        q = """INSERT INTO fred.{} (observation_date, value)
               VALUES {}
               ON CONFLICT (observation_date)
               DO UPDATE SET value = EXCLUDED.value""".format(table_name, values)

        s = text(q)
        logging.debug(s)
        conn.execute(s)
        msg = "Inserted or Updated {} item(s) on table {}.".format(len(df), table_name)
        logging.info(msg)
    else:
        logging.info("Doing full process on {}.".format(table_name))
        q = "TRUNCATE fred.{}".format(table_name)
        conn.execute(q)
        df.to_sql(table_name, engine, schema='fred', if_exists='append', index=False) ## To be used with initial flag
