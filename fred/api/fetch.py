import os
import sys
import json
import urllib.request
import logging

#tests
#refactor
#sql


def url(series_id):
    FRED_API_KEY = os.getenv('FRED_API_KEY', None)
    serie = series_id.upper()
    return "https://api.stlouisfed.org/fred/series/observations?series_id={}&api_key={}&file_type=json".format(serie, FRED_API_KEY)


def fetch_fred_data(series_id):
    serie_url = url(series_id)
    msg = "Fetch URL: {}".format(serie_url)
    logging.debug(msg)
    logging.info("Fetching {} data.".format(series_id))
    serie_json = __fetch_data(serie_url)
    logging.info("Done")
    return json.loads(serie_json)


def __fetch_data(serie_url):
    return urllib.request.urlopen(serie_url).read().decode('utf8')
