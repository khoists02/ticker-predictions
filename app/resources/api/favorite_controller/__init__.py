from flask_restful import Resource
from flask import abort
from webargs import fields
from webargs.flaskparser import use_kwargs, use_args
from resources.models.favorite import Favorite, FavoriteQuery
from resources.helpers import Helpers
import json


class FavoriteController(Resource):
    def __init__(self):
        self.helper = Helpers()

    args = {
        'ticker': fields.Str(
            required=True
        ),
    }

    args_del = {
        'id': fields.Str(
            required=True
        ),
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str):

        qr = FavoriteQuery()
        favorites = qr.findListByTicker(ticker=ticker)
        ids = [i.serialize['id'] for i in favorites]
        symbol_list = [i.serialize['symbol'] for i in favorites]
        url_list = [i.serialize['url_icon'] for i in favorites]

        print(symbol_list)
        rs = []

        for idx, ticker in enumerate(symbol_list):

            # TODO: // will get_daily_info instead when developers fixed
            item = json.loads(self.helper.get_ticker_fast_info(ticker=ticker))
            item["uuid"] = ids[idx]
            item['url_icon'] = url_list[idx]
            item['currentPrice'] = item['lastPrice']
            item['volume'] = item['lastVolume']
            item['bid'] = 0
            item['bidSize'] = 0
            item['ask'] = 0
            item['askSize'] = 0
            item['symbol'] = ticker
            item['shortName'] = ticker
            item['industryDisp'] = "Computer"
            item['recommendationKey'] = None
            item['previousClose'] = item['regularMarketPreviousClose']
            rs.append(item)

        return {
            'content': rs
        }, 200

    @use_kwargs(args_del, location='query')
    def delete(self, id: str):
        qr = FavoriteQuery()
        qr.delete(id)
        return {
            'message': 'Deleted'
        }, 200


class FavoriteAdd(Resource):
    def __init__(self):
        self.helper = Helpers()

    body = {
        'ticker': fields.String(
            required=True,
        )
    }

    @use_args(body)
    def post(self, body):
        qr = FavoriteQuery()
        qr.addNew(ticker=body["ticker"])
        return {
            'message': 'Create Ok !!!'
        }, 201
