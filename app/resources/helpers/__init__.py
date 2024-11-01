"""
Prediction System power by Khoi.le
"""
import numpy as np
from yahoo_fin import stock_info as si
import pandas as pd
import yfinance as yf
from datetime import date

class StockDataService:
    def __init__(self) -> None:
        pass

    def shuffle_in_unison(a, b):
        state = np.random.get_state()
        np.random.shuffle(a)
        np.random.set_state(state)
        np.random.shuffle(b)

    # Return dataFrame of stock data from yahoo_fin.
    @staticmethod
    def load_df_ticker(ticker, start, end):
        if isinstance(ticker, str):
            if start is None:
                start = date.today()

            if end is None:
                end = date.today()
            # load it from yahoo_fin library
            # Interval
            # must be "1d", "1wk", "1mo", or "1m" for daily, weekly, monthly, or minute data.
            # index_as_date Default is True.  If index_as_date = True, then the index of the returned data frame is the date associated with each record.
            # Otherwise, the date is returned as its own column.
            df = si.get_data(ticker, start_date=start,
                             end_date=end, index_as_date=False, interval='1d')
            return df.to_json(orient='records')

        elif isinstance(ticker, pd.DataFrame):
            # already loaded, use it directly
            df = ticker
            return df.to_json(orient='records')
        else:
            raise TypeError(
                "ticker can be either a str or a `pd.DataFrame` instances")

    @staticmethod
    def get_balance_sheet(self, ticker, freq):
        ticker_rs = yf.Ticker(ticker=ticker)
        rs = ticker_rs.get_balance_sheet(freq=freq)
        return rs.to_json()

    @staticmethod
    def get_cash_flow(self, ticker, freq):
        ticker_rs = yf.Ticker(ticker=ticker)
        return ticker_rs.get_cash_flow(freq=freq).to_json()

    @staticmethod
    def get_earning_dates(self, ticker: str):
        ticker_rs = yf.Ticker(ticker=ticker)
        return ticker_rs.get_earnings_dates().to_json(orient='records')

    @staticmethod
    def get_recommendations(self, ticker):
        ticker_rs = yf.Ticker(ticker=ticker)
        return ticker_rs.get_news()

    @staticmethod
    def get_quote_table(self, ticker: str):
        return si.get_quote_table(ticker=ticker)

    @staticmethod
    def get_ticker_daily(self, ticker):
        ticker_rs = yf.Ticker(ticker=ticker)
        rs = ticker_rs.get_info()
        return rs

    @staticmethod
    def get_ticker_fast_info(self, ticker):
        ticker_rs = yf.Ticker(ticker=ticker)
        return ticker_rs.get_fast_info().toJSON()

    @staticmethod
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
