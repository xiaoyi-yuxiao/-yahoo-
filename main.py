import multi as mt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew
from tabulate import tabulate
import datetime as dt
from Analyze import Analyze_Stock


# allow user to input start&end date and interval
def Usr_input():
    # initialize dates
    previousday = dt.date.today() - dt.timedelta(days=1)  # get the date of previous day
    Default_end = previousday.strftime("%Y-%m-%d")  # change the format of the default datetime
    years_ago = dt.date.today() - dt.timedelta(days=5 * 365)
    Default_start = years_ago.strftime("%Y-%m-%d")

    # request user input
    # set default values if users does not enter a value
    Start = input('Enter start date(' + 'Default = 5 Years ago, ' + Default_start + ')-->') or Default_start
    End = input('Enter end date(Default = Yesterday, ' + Default_end + ')-->') or Default_end
    T_interval = input('Enter date interval(1d,1wk,1mo Default = 1mo)-->') or '1mo'

    print("")
    return Start, End, T_interval


# allow user input the stock name
def Stock_input():
    Stock = [input(
        'Please enter ticker ' + str(1) + '(default be AAPL)-->') or 'AAPL',
             input('Please enter ticker ' + str(2) + '(default be MSFT)-->') or 'MSFT']
    return Stock


# return the summary of stock report
def get_all_summary():
    stocks = Stock_input()

    (macro_start, macro_end, macro_T_interval) = Usr_input()

    # get report from SNP market report
    Market_ind = Analyze_Stock('^GSPC', macro_start, macro_end, macro_T_interval)
    M_summary = Market_ind.Get_summary()

    summary_append = [M_summary]
    # append stock report to it
    for i in range(2):
        test = Analyze_Stock(stocks[i], macro_start, macro_end, macro_T_interval)
        summary = test.Get_summary()
        summary_append.append(summary[test.stock])

    summary_append = pd.concat(summary_append, axis=1)
    return summary_append, stocks, macro_start, macro_end, macro_T_interval


# Generate summary measure report
# ask for user input
(Total_summary, stocks, macro_start, macro_end, macro_T_interval) = get_all_summary()

# insert sp500 to stocks
stocks.insert(0, '^GSPC')

print("")
print('             Numerical Summary Measures of Rate of Returns')
print(' ')
print(tabulate(Total_summary, showindex=False, headers=Total_summary.columns, tablefmt="github"))

# print dataset
pd.set_option('display.max_rows', None)
data = mt.download(stocks, start=macro_start, end=macro_end, interval=macro_T_interval)['Adj Close'].dropna()
data = data[[stocks[0], stocks[1], stocks[2]]]  # change arrangement of columns
data.columns = [stocks[0], stocks[1], stocks[2]]  # display short names for index
print("")
print(tabulate(data, showindex=True, headers=data.columns, tablefmt="rst"))
