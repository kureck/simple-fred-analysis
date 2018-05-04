import os
import json
import urllib.request
import pandas as pd
from sqlalchemy import create_engine
#logging
# add last_modified_date

# env varibles
engine = create_engine('postgresql://postgres:postgres@postgres:5432/fred')

# can be transformed into a function
def transform(json_data):
    df = pd.DataFrame(json_data)
    df = df.drop(['realtime_end', 'realtime_start'], axis=1)
    df.rename(columns={'date': 'observation_date'}, inplace=True)
    return df

def update(df, table_name, incremental=False):
    if incremental:
        df.to_sql(table_name, engine, schema='fred', if_exists='append', index=False) ## To be used as incremental
    else:
        df.to_sql(table_name, engine, schema='fred', if_exists='replace', index=False) ## To be used with initial flag

if __name__ == '__main__':
    FRED_API_KEY = os.getenv('FRED_API_KEY', None)

    GDPC1_URL = "https://api.stlouisfed.org/fred/series/observations?series_id=GDPC1&api_key={}&file_type=json".format(FRED_API_KEY)
    UMCSENT_URL = "https://api.stlouisfed.org/fred/series/observations?series_id=UMCSENT&api_key={}&file_type=json".format(FRED_API_KEY)
    UNRATE_URL = "https://api.stlouisfed.org/fred/series/observations?series_id=UNRATE&api_key={}&file_type=json".format(FRED_API_KEY)

    gdpc1_json = urllib.request.urlopen(GDPC1_URL).read().decode('utf8')
    gdpc1 = json.loads(gdpc1_json)

    umcsent_json = urllib.request.urlopen(UMCSENT_URL).read().decode('utf8')
    umcsent = json.loads(gdpc1_json)

    unrate_json = urllib.request.urlopen(UNRATE_URL).read().decode('utf8')
    unrate = json.loads(gdpc1_json)

    gdpc1_df = transform(gdpc1['observations'])
    umcsent_df = transform(umcsent['observations'])
    unrate_df = transform(unrate['observations'])

    update(gdpc1_df, 'gdpc1')
    update(umcsent_df, 'umcsent')
    update(unrate_df, 'unrate')
