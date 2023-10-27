from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs
from resources.models.plays import PlaysQuery
import requests


class PlayDetailsController(Resource):
    def __init__(self):
        self.query = PlaysQuery()

    body = {
        'id': fields.String(
            required=True,
        ),
        'ticker': fields.String(
            required=True,
        ),
        'playedAt': fields.String(
            required=True,
        ),
        'price': fields.Float(
            required=True,
        ),
        'inPrice': fields.Float(
            required=True,
        ),
        'total': fields.Float(
            required=True,
        ),
        'virtual': fields.Boolean(
            required=True,
        ),
        'done': fields.Boolean(
            required=True,
        ),
    }

    def get(self, id):
        return self.query.find_by_id(id), 200

    def delete(self, id):
        self.query.delete(id)
        return {'message': 'deleted'}, 200

    @use_args(body)
    def put(self, body, id):
        self.query.update(id=id, ticker=body['ticker'], price=body['price'],
                          in_price=body['inPrice'], virtual=body['virtual'], played_at=body['playedAt'], done=body['done'], total=body['total'])
        return {'message': 'updated'}, 201


class PlaysController(Resource):
    def __init__(self):
        self.query = PlaysQuery()

    body = {
        'ticker': fields.String(
            required=True,
        ),
        'playedAt': fields.String(
            required=True,
        ),
        'price': fields.Float(
            required=True,
        ),
        'inPrice': fields.Float(
            required=True,
        ),
        'total': fields.Float(
            required=True,
        ),
        'virtual': fields.Boolean(
            required=True,
        ),
        'done': fields.Boolean(
            required=True,
        ),
    }
    args = {
        'ticker': fields.Str(
            required=True
        ),
    }

    @use_kwargs(args, location='query')
    def get(self, ticker):
        rs = self.query.find_all_by_ticker(ticker=ticker)
        return {
            'content': rs
        }, 200

    @use_args(body)
    def post(self, body):
        self.query.create(ticker=body['ticker'], price=body['price'],
                          in_price=body['inPrice'], virtual=body['virtual'], played_at=body['playedAt'], done=body['done'], total=body['total'])

        return {'message': 'OK'}, 201


class PlayTickersController(Resource):
    def __init__(self) -> None:
        self.query = PlaysQuery()

    args = {
        'ticker': fields.Str(
            required=True
        ),
    }

    @use_kwargs(args, location='query')
    def get(self, ticker):
        return {
            'content': self.query.find_all_by_ticker(ticker=ticker)
        }, 200
