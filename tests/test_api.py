import os
from mock import patch
from fred.api.fetch import *


class TestFredApi:
    def setup(self):
        os.environ["FRED_API_KEY"] = '123456abcdef'

    def test_url_is_valid(self):
        series_id = "gdpc1"
        fred_api_key = os.getenv("FRED_API_KEY", None)
        fred_url = url(series_id)

        expected = "https://api.stlouisfed.org/fred/series/observations?series_id={}&api_key={}&file_type=json".format(series_id.upper(), fred_api_key)

        assert fred_url == expected
