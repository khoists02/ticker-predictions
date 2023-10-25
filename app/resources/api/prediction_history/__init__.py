from flask_restful import Resource
from resources.models.predictions_history import PredictionsHistoryQuery
from resources.helpers import Helpers
from webargs import fields
from webargs.flaskparser import use_kwargs
import json


class PredictionsHistory(Resource):
    def __init__(self):
        self.model = PredictionsHistoryQuery()

    def get(self):  # Find all
        return [i.serialize for i in self.model.findAll()], 200


class TickerEarningDates(Resource):
    def __init__(self):
        pass

    args = {
        'ticker': fields.Str(
            required=True
        )
    }

    @use_kwargs(args, location='query')
    def get(self, ticker):  # Find all
        helper = Helpers()
        return helper.get_earning_dates(ticker=ticker), 200
