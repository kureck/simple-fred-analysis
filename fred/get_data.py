import os
import json
import argparse
import urllib.request
import pandas as pd
from sqlalchemy import create_engine

# parser = argparse.ArgumentParser()
# incremental_group = parser.add_mutually_exclusive_group(required=False)
# parser.add_argument('--origin', '-o', help='Origin datasource', required=True)
# parser.add_argument('--target', '-t', help='Target datasource', required=True)
# parser.add_argument('--country', '-c', help='Application country', required=True)
# parser.add_argument('--table', '-T', help='Table name', required=False)
# incremental_group.add_argument('--incremental',
#                                dest='incremental',
#                                action='store_true',
#                                help='Flag to set if job is full or incremental')
# parser.set_defaults(incremental=False)
#
# args = parser.parse_args()
#logging
# add argparse

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
    if incremental:
        # UPSERT
        # https://www.postgresql.org/docs/9.5/static/sql-insert.html
        df.to_sql(table_name, engine, schema='fred', if_exists='append', index=False) ## To be used as incremental
    else:
        # It doesn't creat with constraint :(
        df.to_sql(table_name, engine, schema='fred', if_exists='replace', index=False) ## To be used with initial flag

def url(series_id):
    FRED_API_KEY = os.getenv('FRED_API_KEY', None)
    serie = series_id.upper()
    return "https://api.stlouisfed.org/fred/series/observations?series_id={}&api_key={}&file_type=json".format(serie, FRED_API_KEY)

def fetch_data(series_id):
    serie_url = url(series_id)

    serie_json = urllib.request.urlopen(serie_url).read().decode('utf8')
    return json.loads(serie_json)

if __name__ == '__main__':
    gdpc1 = fetch_data('gdpc1')
    umcsent = fetch_data('umcsent')
    unrate = fetch_data('unrate')

    gdpc1_df = transform(gdpc1['observations'])
    umcsent_df = transform(umcsent['observations'])
    unrate_df = transform(unrate['observations'])

    import ipdb; ipdb.set_trace()

    update(gdpc1_df, 'gdpc1')
    update(umcsent_df, 'umcsent')
    update(unrate_df, 'unrate')
