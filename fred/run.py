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
parser.add_argument('--start_date', '-st', help='Start date', required=False, default='1776-07-04')
parser.add_argument('--end_date', '-e', help='End date', required=False, default='9999-12-31')
parser.add_argument('--log-level', '-l', help='Log Level', required=False, default='INFO')
incremental_group.add_argument('--incremental',
                               dest='incremental',
                               action='store_true',
                               help='Flag to set if job is full or incremental')
parser.set_defaults(incremental=False)

args = parser.parse_args()


def set_log(log_level='INFO'):
    """Set log level."""
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
    serie_data = fetch_fred_data(args.serie, start_date=args.start_date, end_date=args.end_date)
    df = transform(serie_data['observations'])

    update(df, args.table, args.incremental)
