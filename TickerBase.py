from __future__ import print_function

import time as _time
import datetime as _datetime
import requests as _requests
import pandas as pd
import numpy as np
import Utils as _Utils

try:
    from urllib.parse import quote as urlencode
except ImportError:
    from urllib import quote as urlencode


class TickerBase:
    def __init__(self, ticker):
        # get every ticker to upper case
        self.ticker = ticker.upper()
        self._history = None
        self._base_url = 'https://query1.finance.yahoo.com'

    def history(self, interval="1d",
                start=None, end=None):
        """:parameter:
            interval : str
                valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            start : str
                Download starting date(YYYY-MM-DD)
                default is 1900-01-01
            end : str
                Download ending date(YYYY-MM-DD)
                default now
        """
        if start is None:
            start = -2208988800
        elif isinstance(start, _datetime.datetime):
            start = int(_time.mktime(start.timetuple()))
        else:
            # inverse the str to epoch time
            start = int(_time.mktime(
                _time.strptime(str(start), '%Y-%m-%d')
            ))

        if end is None:
            end = int(_time.time())
        elif isinstance(end, _datetime.datetime):
            end = int(_time.mktime(end.timetuple()))
        else:
            end = int(_time.mktime(_time.strptime(str(end), '%Y-%m-%d')))

        params = {"period1": start, "period2": end, "interval": interval.lower()}

        # getting data from json
        url = "{}/v8/finance/chart/{}".format(self._base_url, self.ticker)
        data = _requests.get(url=url, params=params)
        data = data.json()

        # parse quotes
        quotes = _Utils.parse_quotes(data["chart"]["result"][0])
        quotes.dropna(inplace=True)

        self._history = quotes.copy()

        return quotes

