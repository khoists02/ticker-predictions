from flask_restful import Resource
from flask import abort
from webargs import fields
from webargs.flaskparser import use_kwargs
from resources.models.report import ReportQuery
from resources.helpers import Helpers
import json

"""
TickerFastInfoController
get fast info from yahoo finance API
"""


class TickerFastInfoController(Resource):
    def __init__(self):
        self.helper = Helpers()

    args = {
        'ticker': fields.Str(
            required=True
        ),
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str):
        rs = json.loads(self.helper.get_ticker_fast_info(ticker=ticker))
        print(rs['lastPrice'])
        rs['currentPrice'] = rs['lastPrice']
        rs['volume'] = rs['lastVolume']
        rs['bid'] = 0
        rs['bidSize'] = 0
        rs['ask'] = 0
        rs['askSize'] = 0
        rs['symbol'] = ticker
        rs['shortName'] = "BLND Labs."
        rs['industryDisp'] = "Computer"
        rs['recommendationKey'] = None
        return {
            'content': rs
        }, 200
