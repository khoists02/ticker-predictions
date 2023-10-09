from flask_restful import Resource
from flask import abort
from webargs import fields
from webargs.flaskparser import use_kwargs


class TickerSettings(Resource):
    def __init__(self):
        pass

    def get(self):
        return [{"ticker": "BLND", "short": "Blend Labs, Inc."}], 200


class TickersAccount(Resource):
    def __init__(self):
        pass

    args = {
        'ticker': fields.Str(
            required=True
        ),
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str):
        return {
            "balance": 4366.65,
            "current": 5.49,
            "ticker": ticker
        }, 200
