from flask_restful import Resource
from flask import abort
from webargs import fields
from webargs.flaskparser import use_kwargs, use_args
from resources.models.favorite import Favorite, FavoriteQuery
from resources.helpers import Helpers


class FavoriteController(Resource):
    def __init__(self):
        self.helper = Helpers()

    args = {
        'ticker': fields.Str(
            required=True
        ),
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str):

        qr = FavoriteQuery()
        favorites = qr.findListByTicker(ticker=ticker)
        symbol_list = [i.serialize['symbol'] for i in favorites]

        print(symbol_list)
        rs = []

        for ticker in symbol_list:
            rs.append(self.helper.get_ticker_daily(ticker=ticker))

        return {
            'content': rs
        }, 200
