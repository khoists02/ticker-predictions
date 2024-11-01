"""
Prediction System power by Khoi.le
"""
from flask_restful import Resource
import json
from resources.helpers import StockDataService
from webargs import fields
from webargs.flaskparser import use_kwargs

class StockData(Resource):
    def __init__(self) -> None:
        self.stock_service = StockDataService()

    args = {
        'ticker': fields.Str(
            required=True
        ),
        'start': fields.Str(
            required=True,
            default=None
        ),
        'end': fields.Str(
            required=True,
            default=None
        ),
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str, start, end):
        try:
            data = self.stock_service.load_df_ticker(
                ticker=ticker, start=start, end=end)
            return json.loads(data), 200
        except Exception as e:
            return e, 500


class StockInfo(Resource):
    def __init__(self) -> None:
        self.stock_service = StockDataService()

    args = {
        'ticker': fields.Str(
            required=True
        )
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str):
        return self.stock_service.get_ticker_daily(ticker=ticker), 200


class StockBalanceSheet(Resource):
    def __init__(self) -> None:
        self.stock_service = StockDataService()

    args = {
        'ticker': fields.Str(
            required=True
        ),
        'freq': fields.Str(
            required=True
        )
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str, freq: str):
        return json.loads(self.stock_service.get_balance_sheet(ticker=ticker, freq=freq)), 200


class StockCashFlowSheet(Resource):
    def __init__(self) -> None:
        self.stock_service = StockDataService()

    args = {
        'ticker': fields.Str(
            required=True
        ),
        'freq': fields.Str(
            required=True
        )
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str, freq: str):
        return json.loads(self.stock_service.get_cash_flow(ticker=ticker, freq=freq))


class StockRecommendations(Resource):
    def __init__(self) -> None:
        self.stock_service = StockDataService()

    args = {
        'ticker': fields.Str(
            required=True
        )
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str):
        return self.stock_service.get_recommendations(ticker=ticker)


class StockDataDaily(Resource):
    def __init__(self) -> None:
        self.stock_service = StockDataService()

    args = {
        'ticker': fields.Str(
            required=True
        ),
        'start': fields.Str(
            required=True,
            default=None
        ),
        'end': fields.Str(
            required=True,
            default=None
        ),
        'interval': fields.Str(
            required=True,
            default=None
        ),
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str, start, end, interval):
        try:
            data = self.stock_service.load_stock_by_day(
                ticker=ticker, start=start, end=end, interval=interval)
            return json.loads(data), 200
        except Exception as e:
            return e, 500
