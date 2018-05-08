import os
from mock import patch
from fred.api.fetch import *


class TestFredApi:
    def setup(self):
        os.environ["FRED_API_KEY"] = '123456abcdef'

    def test_url_is_valid(self):
        series_id = "gdpc1"
        start_date = '1900-01-01'
        end_date = '2000-01-01'
        fred_api_key = os.getenv("FRED_API_KEY", None)
        fred_url = url(series_id, start_date, end_date)

        expected = "https://api.stlouisfed.org/fred/series/observations?series_id={}&observation_start={}&observation_end={}&api_key={}&file_type=json".format(series_id.upper(), start_date, end_date, fred_api_key)

        assert fred_url == expected
