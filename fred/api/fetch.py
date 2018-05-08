import os
import sys
import json
import urllib.request
import logging


def url(series_id, start_date, end_date):
    """Generates a url based on series_id and FRED_API_KEY."""
    FRED_API_KEY = os.getenv('FRED_API_KEY', None)
    serie = series_id.upper()
    return "https://api.stlouisfed.org/fred/series/observations?series_id={}&observation_start={}&observation_end={}&api_key={}&file_type=json".format(serie, start_date, end_date, FRED_API_KEY)


def fetch_fred_data(series_id, start_date='1776-07-04', end_date='9999-12-31'):
    """Fetches data from fred api and returns a json object."""
    serie_url = url(series_id, start_date, end_date)
    msg = "Fetch URL: {}".format(serie_url)
    logging.debug(msg)
    logging.info("Fetching {} data.".format(series_id))
    serie_json = __fetch_data(serie_url)
    logging.info("Done")
    return json.loads(serie_json)


def __fetch_data(serie_url):
    return urllib.request.urlopen(serie_url).read().decode('utf8')
