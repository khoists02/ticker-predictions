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

    del_args = {
        'id': fields.Str(
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

    update_body = {
        'id': fields.String(
            required=True,
        ),
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

    def get_updated(item):
        return item.get('updated_at')

    @use_kwargs(args, location='query')
    def get(self, ticker):
        qr = BidAskQuery()
        list = qr.findListByTicker(ticker=ticker)
        rs = [i.serialize for i in list]
        # print(rs)
        # print()
        return {
            'content': sorted(rs, key=lambda x: x['updatedAt']),
        }, 200

    @use_args(update_body)
    def put(self, body):
        qr = BidAskQuery()
        qr.update(id=body['id'], ticker=body['ticker'], ask=body['ask'], bid=body['bid'],
                  ask_size=body['askSize'], bid_size=body['bidSize'], updated_at=body['updatedAt'])
        return {'message': 'Update Success'}, 201

    @use_args(body)
    def post(self, body):
        qr = BidAskQuery()
        count: int = qr.create(ticker=body['ticker'], ask=body['ask'], bid=body['bid'],
                               ask_size=body['askSize'], bid_size=body['bidSize'], updated_at=body['updatedAt'])
        if count == 0:
            return {'message': 'Exits'}, 400
        return {'message': 'Create Success'}, 201

    @use_kwargs(del_args, location='query')
    def delete(self, id):
        qr = BidAskQuery()
        qr.delete(id=id)
        return {
            'message': 'OK'
        }, 201


class BidAsksDetails(Resource):
    def __init__(self) -> None:
        pass

    # args = {
    #     'id': fields.Str(
    #         required=True
    #     ),
    # }

    # @use_kwargs(args, location='query')
    def get(self, id: str):
        qr = BidAskQuery()
        rs = qr.findById(id)
        return rs
