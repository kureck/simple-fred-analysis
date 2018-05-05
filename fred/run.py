import argparse
from get_data import *

parser = argparse.ArgumentParser()
incremental_group = parser.add_mutually_exclusive_group(required=False)
parser.add_argument('--serie', '-s', help='Serie observed datasource', required=True)
parser.add_argument('--table', '-t', help='Table name', required=True)
incremental_group.add_argument('--incremental',
                               dest='incremental',
                               action='store_true',
                               help='Flag to set if job is full or incremental')
parser.set_defaults(incremental=False)

args = parser.parse_args()

if __name__ == '__main__':
    serie_data = fetch_data(args.serie)
    df = transform(serie_data['observations'])

    # data = [{'observation_date': '1947-01-01', 'value': 2999.0}, {'observation_date': '1947-02-01', 'value': 3000.0}]
    # df = pd.DataFrame(data)
    update(df, args.table, args.incremental)

    # gdpc1 = fetch_data('gdpc1')
    # umcsent = fetch_data('umcsent')
    # unrate = fetch_data('unrate')
    #
    # gdpc1_df = transform(gdpc1['observations'])
    # umcsent_df = transform(umcsent['observations'])
    # unrate_df = transform(unrate['observations'])
    #
    # import ipdb; ipdb.set_trace()
    #
    # update(gdpc1_df, 'gdpc1', True)
    # update(umcsent_df, 'umcsent')
    # update(unrate_df, 'unrate')
