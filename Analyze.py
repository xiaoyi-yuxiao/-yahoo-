import multi as mt
import numpy as np
import pandas as pd
from scipy.stats import kurtosis, skew

class Analyze_Stock:

    def __init__(self, Stock_Name, Start_T, End_T, T_Interval):
        self.__Stock_price = mt.download(Stock_Name, start=Start_T, end=End_T, interval=T_Interval)[
            'Adj Close'].dropna().squeeze()
        self.__Ret = self.__Stock_price.pct_change()[1:]

        monthly_data = mt.download(Stock_Name, start=Start_T, end=End_T, interval='1mo')['Adj Close'].dropna().squeeze()
        slice_object = slice(1, len(monthly_data), 12)

        self.__Yr_Ret = monthly_data[slice_object].pct_change()[1:]
        self.__count = len(self.__Stock_price)
        self.stock = Stock_Name
        self.start = Start_T
        self.end = End_T
        self.frequency = T_Interval

    def __helper(self, N):
        return '{:0.3%}'.format(N)

    def __helper_2(self, N):
        return '{:0.2f}'.format(N)

    def __helper_4(self, N):
        return '{:0.4}'.format(N)

    def Mean_Ret(self):
        mean = np.mean(self.__Ret)
        return mean

    def Median_Ret(self):
        median = np.median(self.__Ret)
        return median

    def STD_Ret(self):
        std = np.std(self.__Ret)
        return std

    def Var_Ret(self):
        Var = np.var(self.__Ret)
        return Var

    def Annual_Mean_Ret(self):
        mean = np.mean(self.__Yr_Ret)
        return mean

    def Annual_Median_Ret(self):
        median = np.median(self.__Yr_Ret)
        return median

    def Annual_Std(self):
        std = np.std(self.__Yr_Ret)
        return std

    def Annual_Var(self):
        var = np.var(self.__Yr_Ret)
        return var

    def Min_Ret(self):
        Min = min(self.__Yr_Ret)
        return Min

    def Max_Ret(self):
        Max = max(self.__Yr_Ret)
        return Max

    def Range_Ret(self):
        Range = max(self.__Yr_Ret) - min(self.__Yr_Ret)
        return Range

    def Min_Price(self):
        Min = min(self.__Stock_price)
        return Min

    def Max_Price(self):
        Max = max(self.__Stock_price)
        return Max

    def Range_Price(self):
        Range = max(self.__Stock_price) - min(self.__Stock_price)
        return Range

    def quarter_tile(self):
        quarter = np.quantile(self.__Ret, 0.25)
        return quarter

    def half_tile(self):
        half = np.quantile(self.__Ret, 0.5)
        return half

    def Tquarter_tile(self):
        Tquarter = np.quantile(self.__Ret, 0.75)
        return Tquarter

    def interquatile(self):
        Int_quarter = np.quantile(self.__Ret, 0.75) - np.quantile(self.__Ret, 0.25)
        return Int_quarter

    def kurt(self):
        Kurt = kurtosis(self.__Stock_price)
        return Kurt

    def skewness(self):
        Skew = skew(self.__Stock_price)
        return Skew

    def get_count(self):
        return self.__count

    def CoV(self):
        cov = np.std(self.__Ret) - np.mean(self.__Ret)
        return cov

    # calculate correlation coefficient
    def Market_corr(self):
        SNP = mt.download('^GSPC', start=self.start, end=self.end, interval=self.frequency)['Adj Close'].dropna().squeeze()
        corr = np.corrcoef(SNP, self.__Stock_price)
        return corr[0, 1]

    def Get_summary(self):
        dict_data = {
            'Measures': ['Start Date', 'End Date', 'Frequency', 'Mean Return', 'Median Return', 'Standard deviation',
                         'Variance', 'Annual Mean Return', 'Median Annual Return', 'Annual Standard Deviation',
                         'Annual Variance', 'Minimum Return', 'Maximum Return', 'Range Return', 'Minimum Price',
                         'Maximum Price', 'Range Price', 'Quatile 25%', 'Quatile 50%', 'Quatile 75%', 'Interquartile',
                         'Kurtosis', 'Skewness', 'Count', 'Coefficient of Variation', 'Market corr with S&P 500'],
            self.stock: [self.start, self.end, self.frequency, self.__helper(self.Mean_Ret()),
                         self.__helper(self.Median_Ret()),
                         self.__helper(self.STD_Ret()), self.__helper(self.Var_Ret()),
                         self.__helper(self.Annual_Mean_Ret()),
                         self.__helper(self.Annual_Median_Ret()), self.__helper(self.Annual_Std()),
                         self.__helper(self.Annual_Var()),
                         self.__helper(self.Min_Ret()), self.__helper(self.Max_Ret()), self.__helper(self.Range_Ret()),
                         self.__helper_2(self.Min_Price()),
                         self.__helper_2(self.Max_Price()), self.__helper_2(self.Range_Price()),
                         self.__helper(self.quarter_tile()), self.__helper(self.half_tile()),
                         self.__helper(self.Tquarter_tile()), self.__helper(self.interquatile()),
                         self.__helper_4(self.kurt()),
                         self.__helper_4(self.skewness()), self.get_count(), self.__helper_4(self.CoV()),
                         self.__helper_4(self.Market_corr())]
        }
        frame_data = pd.DataFrame(dict_data)
        print(self.__Stock_price)
        print(self.__Ret)
        return frame_data
