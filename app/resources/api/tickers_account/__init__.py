from flask_restful import Resource
from flask import abort
from webargs import fields
from webargs.flaskparser import use_kwargs, use_args
from resources.api.settings import SettingQuery, Settings


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

    body = {
        'balance': fields.Float(
            required=True
        ),
        'current': fields.Float(
            required=True
        ),
        'id': fields.Str(
            required=True
        ),
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str):

        qr = SettingQuery()
        settings: Settings = qr.findByTicker(ticker=ticker)
        return {
            "balance": settings.balance,
            "current": settings.current,
            "ticker": settings.ticker,
        }, 200

    @use_args(body)
    def put(self, body):
        print(body)
        qr = SettingQuery()
        qr.updateSetting(
            id=body["id"], balance=body["balance"], current=body["current"])
        return {
            "message": "ok",
        }, 201
