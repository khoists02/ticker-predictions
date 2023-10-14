from flask_restful import Resource
from flask import abort
from webargs import fields
from webargs.flaskparser import use_kwargs, use_args
from resources.models.notification import Notification, NotificationQuery
from resources.helpers import Helpers


class NotificationController(Resource):
    def __init__(self):
        self.helper = Helpers()

    args = {
        'ticker': fields.Str(
            required=True
        ),
    }

    body = {
        'ticker': fields.String(
            required=True,
        ),
        'per': fields.Float(
            required=True,
        ),
        'close': fields.Float(
            required=True
        ),
        'updatedAt': fields.Str(
            required=True
        ),
    }

    def get(self):
        qr = NotificationQuery()
        notifications = qr.findAll()
        return {
            'content': [i.serialize for i in notifications]
        }, 200

    @use_args(body)
    def post(self, body):
        qr = NotificationQuery()
        qr.createOne(body=body)
        return {'message': 'Create Success'}, 201


class NotificationCount(Resource):
    def __init__(self) -> None:
        pass

    def get(self):
        qr = NotificationQuery()
        rs = qr.count()
        return {
            'count': rs
        }, 200


class NotificationDetails(Resource):
    def __init__(self):
        pass

    # body = {
    #     'read': fields.Bool(
    #         required=True,
    #     ),
    # }

    def put(self, id):
        qr = NotificationQuery()
        print(id)
        qr.read(id=id)
        return {'message': 'No Content'}, 200
