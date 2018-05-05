import os
import json
import urllib.request
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text

#logging

def db_engine():
    DB_HOST = os.getenv('DB_HOST', None)
    DB_PORT = os.getenv('DB_PORT', None)
    DB_USER = os.getenv('DB_USER', None)
    DB_PASSWD = os.getenv('DB_PASSWD', None)
    DB_NAME = os.getenv('DB_NAME', None)
    connection_url = 'postgresql://{}:{}@{}:{}/{}'.format(DB_USER, DB_PASSWD, DB_HOST, DB_PORT, DB_NAME)
    return create_engine(connection_url)

def transform(json_data):
    df = pd.DataFrame(json_data)
    df = df.drop(['realtime_end', 'realtime_start'], axis=1)
    df.rename(columns={'date': 'observation_date'}, inplace=True)
    return df

def update(df, table_name, incremental=False):
    engine = db_engine()
    conn = engine.connect()
    if incremental:
        values = ""
        for value in df.values:
            values += "('{}', '{}'),".format(value[0], value[1])
        values = values.strip(",")
        q = """INSERT INTO fred.{} (observation_date, value)
                    VALUES {}
                    ON CONFLICT (observation_date)
                    DO UPDATE SET value = EXCLUDED.value""".format(table_name, values)

        s = text(q)
        conn.execute(s)
    else:
        q = "TRUNCATE fred.{}".format(table_name)
        conn.execute(q)
        df.to_sql(table_name, engine, schema='fred', if_exists='append', index=False) ## To be used with initial flag

def url(series_id):
    FRED_API_KEY = os.getenv('FRED_API_KEY', None)
    serie = series_id.upper()
    return "https://api.stlouisfed.org/fred/series/observations?series_id={}&api_key={}&file_type=json".format(serie, FRED_API_KEY)

def fetch_data(series_id):
    serie_url = url(series_id)

    serie_json = urllib.request.urlopen(serie_url).read().decode('utf8')
    return json.loads(serie_json)
