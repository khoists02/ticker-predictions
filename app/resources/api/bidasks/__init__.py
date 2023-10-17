from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs
from resources.models.bidask import BidAskQuery


class BidAskController(Resource):
    def __init__(self):
        pass

    args = {
        'ticker': fields.Str(
            required=True
        ),
    }

    body = {
        'ticker': fields.String(
            required=True,
        ),
        'updatedAt': fields.String(
            required=True,
        ),
        'ask': fields.Float(
            required=True
        ),
        'bid': fields.Float(
            required=True
        ),
        'askSize': fields.Float(
            required=True
        ),
        'bidSize': fields.Float(
            required=True
        ),
    }

    @use_kwargs(args, location='query')
    def get(self, ticker):
        qr = BidAskQuery()
        list = qr.findListByTicker(ticker=ticker)
        return {
            'content': [i.serialize for i in list]
        }, 200

    @use_args(body)
    def post(self, body):
        qr = BidAskQuery()
        count: int = qr.create(ticker=body['ticker'], ask=body['ask'], bid=body['bid'],
                               ask_size=body['askSize'], bid_size=body['bidSize'], updated_at=body['updatedAt'])
        if count == 0:
            return {'message': 'Exits'}, 400
        return {'message': 'Create Success'}, 201
