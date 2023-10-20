import numpy as np
from flask_restful import abort
from yahoo_fin import stock_info as si
# from sklearn import preprocessing
# from sklearn.model_selection import train_test_split
import pandas as pd
from collections import deque
import yfinance as yf
from datetime import date
import json
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'


class Helpers:
    def __init__(self) -> None:
        pass

    def shuffle_in_unison(a, b):
        # shuffle two arrays in the same way
        state = np.random.get_state()
        np.random.shuffle(a)
        np.random.set_state(state)
        np.random.shuffle(b)

    def load_df_ticker(self, ticker, start, end):
        if isinstance(ticker, str):
            if start is None:
                start = date.today()

            if end is None:
                end = date.today()
            # load it from yahoo_fin library
            # Interval
            # must be "1d", "1wk", "1mo", or "1m" for daily, weekly, monthly, or minute data.
            df = si.get_data(ticker, start_date=start,
                             end_date=end, index_as_date=False)
            return df.to_json(orient='records')

        elif isinstance(ticker, pd.DataFrame):
            # already loaded, use it directly
            df = ticker
            return df.to_json(orient='records')
        else:
            raise TypeError(
                "ticker can be either a str or a `pd.DataFrame` instances")

    # def load_stock_data(self, ticker, n_steps=50, scale=True, shuffle=True, lookup_step=1, split_by_date=True,
    #                     test_size=0.2, feature_columns=['adjclose', 'volume', 'open', 'high', 'low']):
    #     if isinstance(ticker, str):
    #         # load it from yahoo_fin library
    #         df = si.get_data(ticker)
    #     elif isinstance(ticker, pd.DataFrame):
    #         # already loaded, use it directly
    #         df = ticker
    #     else:
    #         raise TypeError(
    #             "ticker can be either a str or a `pd.DataFrame` instances")

    #     # this will contain all the elements we want to return from this function
    #     result = {}
    #     # we will also return the original dataframe itself
    #     result['df'] = df.copy()
    #     # make sure that the passed feature_columns exist in the dataframe
    #     for col in feature_columns:
    #         assert col in df.columns, f"'{col}' does not exist in the dataframe."
    #     # add date as a column
    #     if "date" not in df.columns:
    #         df["date"] = df.index
    #     if scale:
    #         column_scaler = {}
    #         # scale the data (prices) from 0 to 1
    #         for column in feature_columns:
    #             scaler = preprocessing.MinMaxScaler()
    #             df[column] = scaler.fit_transform(
    #                 np.expand_dims(df[column].values, axis=1))
    #             column_scaler[column] = scaler
    #         # add the MinMaxScaler instances to the result returned
    #         result["column_scaler"] = column_scaler
    #     # add the target column (label) by shifting by `lookup_step`
    #     df['future'] = df['adjclose'].shift(-lookup_step)
    #     # last `lookup_step` columns contains NaN in future column
    #     # get them before droping NaNs
    #     last_sequence = np.array(df[feature_columns].tail(lookup_step))
    #     # drop NaNs
    #     df.dropna(inplace=True)
    #     sequence_data = []
    #     sequences = deque(maxlen=n_steps)
    #     for entry, target in zip(df[feature_columns + ["date"]].values, df['future'].values):
    #         sequences.append(entry)
    #         if len(sequences) == n_steps:
    #             sequence_data.append([np.array(sequences), target])
    #     # get the last sequence by appending the last `n_step` sequence with `lookup_step` sequence
    #     # for instance, if n_steps=50 and lookup_step=10, last_sequence should be of 60 (that is 50+10) length
    #     # this last_sequence will be used to predict future stock prices that are not available in the dataset
    #     last_sequence = list([s[:len(feature_columns)]
    #                          for s in sequences]) + list(last_sequence)
    #     last_sequence = np.array(last_sequence).astype(np.float32)
    #     # add to result
    #     result['last_sequence'] = last_sequence
    #     # construct the X's and y's
    #     X, y = [], []
    #     for seq, target in sequence_data:
    #         X.append(seq)
    #         y.append(target)
    #     # convert to numpy arrays
    #     X = np.array(X)
    #     y = np.array(y)
    #     if split_by_date:
    #         # split the dataset into training & testing sets by date (not randomly splitting)
    #         train_samples = int((1 - test_size) * len(X))
    #         result["X_train"] = X[:train_samples]
    #         result["y_train"] = y[:train_samples]
    #         result["X_test"] = X[train_samples:]
    #         result["y_test"] = y[train_samples:]
    #         if shuffle:
    #             # shuffle the datasets for training (if shuffle parameter is set)
    #             self.shuffle_in_unison(result["X_train"], result["y_train"])
    #             self.shuffle_in_unison(result["X_test"], result["y_test"])
    #     else:
    #         # split the dataset randomly
    #         result["X_train"], result["X_test"], result["y_train"], result["y_test"] = train_test_split(X, y,
    #                                                                                                     test_size=test_size, shuffle=shuffle)
    #     # get the list of test set dates
    #     dates = result["X_test"][:, -1, -1]
    #     # retrieve test features from the original dataframe
    #     result["test_df"] = result["df"].loc[dates]
    #     # remove duplicated dates in the testing dataframe
    #     result["test_df"] = result["test_df"][~result["test_df"].index.duplicated(
    #         keep='first')]
    #     # remove dates from the training/testing sets & convert to float32
    #     result["X_train"] = result["X_train"][:, :,
    #                                           :len(feature_columns)].astype(np.float32)
    #     result["X_test"] = result["X_test"][:, :,
    #                                         :len(feature_columns)].astype(np.float32)
    #     return result

    def get_balance_sheet(self, ticker, freq):
        ticker_rs = yf.Ticker(ticker=ticker)
        rs = ticker_rs.get_balance_sheet(freq=freq)
        return rs.to_json()

    def get_cash_flow(self, ticker, freq):
        ticker_rs = yf.Ticker(ticker=ticker)
        return ticker_rs.get_cash_flow(freq=freq).to_json()

    def get_earning_dates(self, ticker: str):
        ticker_rs = yf.Ticker(ticker=ticker)
        return ticker_rs.get_earnings_dates().to_json()

    def get_recommendations(self, ticker):
        ticker_rs = yf.Ticker(ticker=ticker)
        return ticker_rs.get_news()

    def get_quote_table(self, ticker: str):
        return si.get_quote_table(ticker=ticker)

    def get_ticker_daily(self, ticker):
        ticker_rs = yf.Ticker(ticker=ticker)
        rs = ticker_rs.get_info()
        return rs

    def get_ticker_fast_info(self, ticker):
        ticker_rs = si.Ticker(ticker=ticker)
        return ticker_rs.get_fast_info().toJSON()

    def load_stock_by_day(self, ticker, start, end, interval):
        ticker_rs = yf.Ticker(ticker=ticker)
        if isinstance(ticker, str):
            print("start")
            if start is None:
                start = date.today()

            if end is None:
                end = date.today()
            # load it from yahoo_fin library
            # Interval
            # Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            print(start, end)
            df = ticker_rs.history(start=start, end=end,
                                   interval=interval, period="max")

            print("loaded!!!")
            return df.to_json(orient='records')

        elif isinstance(ticker, pd.DataFrame):
            # already loaded, use it directly
            df = ticker
            return df.to_json(orient='records')
        else:
            raise TypeError(
                "ticker can be either a str or a `pd.DataFrame` instances")
