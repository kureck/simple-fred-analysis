import pandas as pd


def transform(json_data):
    """Removes unused column and rename date column."""
    df = pd.DataFrame(json_data)
    df = df.drop(['realtime_end', 'realtime_start'], axis=1)
    df.rename(columns={'date': 'observation_date'}, inplace=True)
    return df
