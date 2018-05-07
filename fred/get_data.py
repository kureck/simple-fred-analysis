import os
import sys
import json
import urllib.request
import logging
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.sql import text

#tests
#refactor
#sql


def set_log(log_level='INFO'):
    log_level_number = log_level.upper()
    if not isinstance(log_level_number, int):
        print('ERROR: Invalid log level {}'.format(log_level.upper()))
        sys.exit(-1)
    logging.basicConfig(level=log_level.upper(),
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%y/%m/%d %H:%M:%S',
                        stream=sys.stdout)
    logging.StreamHandler(sys.stdout)
