import sys
import argparse
import logging
from api.fetch import fetch_fred_data
from transform.transform import transform
from db.db import update

parser = argparse.ArgumentParser()
incremental_group = parser.add_mutually_exclusive_group(required=False)
parser.add_argument('--serie', '-s', help='Serie observed datasource', required=True)
parser.add_argument('--table', '-t', help='Table name', required=True)
parser.add_argument('--log-level', '-l', help='Log Level', required=False, default='INFO')
incremental_group.add_argument('--incremental',
                               dest='incremental',
                               action='store_true',
                               help='Flag to set if job is full or incremental')
parser.set_defaults(incremental=False)

args = parser.parse_args()


def set_log(log_level='INFO'):
    level = {'CRITICAL': 50, 'ERROR': 40,
             'WARNING': 30, 'INFO': 20, 'DEBUG': 10}
    log_level_number = level[log_level.upper()]
    if not isinstance(log_level_number, int):
        print('ERROR: Invalid log level {}'.format(log_level.upper()))
        sys.exit(-1)
    logging.basicConfig(level=log_level.upper(),
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%y/%m/%d %H:%M:%S',
                        stream=sys.stdout)
    logging.StreamHandler(sys.stdout)

if __name__ == '__main__':
    set_log(args.log_level)
    serie_data = fetch_fred_data(args.serie)
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
