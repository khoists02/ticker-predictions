from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from resources.models.plays import PlaysQuery


class PlayDetailsController(Resource):
    def __init__(self):
        self.query = PlaysQuery()

    body = {
        'ticker': fields.String(
            required=True,
        ),
        'played_at': fields.String(
            required=True,
        ),
        'price': fields.Float(
            required=True,
        ),
        'in_price': fields.Float(
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
    def put(self, id, body):
        self.query.update(id=id, ticker=body['ticker'], price=body['price'],
                          in_price=body['in_price'], virtual=body['virtual'], played_at=body['played_at'], done=body['done'], total=body['total'])
        return {'message': 'updated'}, 201


class PlaysController(Resource):
    def __init__(self):
        self.query = PlaysQuery()

    body = {
        'ticker': fields.String(
            required=True,
        ),
        'played_at': fields.String(
            required=True,
        ),
        'price': fields.Float(
            required=True,
        ),
        'in_price': fields.Float(
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

    def get(self):
        rs = self.query.find_all()
        return {
            'content': rs
        }, 200

    @use_args(body)
    def post(self, body):
        self.query.create(ticker=body['ticker'], price=body['price'],
                          in_price=body['in_price'], virtual=body['virtual'], played_at=body['played_at'], done=body['done'], total=body['total'])

        return {'message': 'OK'}, 201
