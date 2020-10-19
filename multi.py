from __future__ import print_function

import time as _time
import multitasking as _multitasking
import pandas as _pd

from TickerBase import TickerBase
import Utils as _Utils

# create empty dict for dataframes
_DFS = {}


def download(tickers, start=None, end=None, threads=True,
             group_by='column',
             interval="1d"):
    """Download tickers
    :parameter
        tickers: str,list
            List of tickers to be dowmload
        interval: str
            default same as ticker
        start: str
            default same as ticker
        end: str
            default same as ticker
        threads:bool
            multi threads downloading,default be true
    """
    global _DFS

    # reset DFS
    _DFS = {}

    # create ticker list
    tickers = tickers if isinstance(
        tickers, (list, set, tuple)
    ) else tickers.replace(',', ' ').split()

    tickers = list(set([ticker.upper() for ticker in tickers]))

    # download using threads
    if threads:
        # set the threads
        threads = min([len(tickers), _multitasking.cpu_count() * 2])
        # set the maximum threads
        _multitasking.set_max_threads(threads)
        for i, ticker in enumerate(tickers):
            _download_one_threaded(ticker=ticker, start=start, end=end, interval=interval)
        while len(_DFS) < len(tickers):
            _time.sleep(0.01)

    else:
        for i, ticker in enumerate(tickers):
            data = _download_one(ticker,start=start,end=end,interval=interval)
            _DFS[ticker.upper()] = data

    # concating the results
    try:
        data = _pd.concat(_DFS.values(), axis=1, keys=_DFS.keys())
    except Exception:
        data = _pd.concat(_DFS.values(), axis=1, keys=_DFS.keys())

    if group_by == 'column':
        data.columns = data.columns.swaplevel(0,1)
        data.sort_index(level=0, axis=1, inplace=True)

    return data


def _realign_dfs():
    global _DFS

    idx_len = 0
    idx = None

    for df in _DFS.values():
        if len(df) > idx_len:
            idx_len = len(df)
            idx = df.index

    for key in _DFS.keys():
        try:
            _DFS[key] = _pd.DataFrame(
                index=idx, data=_DFS[key]
            ).drop_duplicates()
        except Exception:
            _DFS[key] = _pd.concat(
                [_Utils.empty_df(idx), _DFS[key].dropna()], axis=0, sort=True
            )
        # remove duplicate index
        _DFS[key] = _DFS[key].loc[
            _DFS[key].index.duplicated(keep='last')
        ]


@_multitasking.task
def _download_one_threaded(ticker, start=None, end=None,
                           interval="1d"):
    global _DFS
    data = _download_one(ticker=ticker, start=start, end=end, interval=interval)
    _DFS[ticker.upper()] = data


def _download_one(ticker, start=None, end=None,
                  interval='1d'):
    return TickerBase(ticker).history(interval=interval, start=start, end=end)


