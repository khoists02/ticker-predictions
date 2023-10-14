from flask_restful import Resource
from webargs import fields
from webargs.flaskparser import use_args
from resources.models.notification import NotificationQuery
from resources.helpers import Helpers
import mailtrap as mt


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
        # mail = mt.Mail(
        #     sender=mt.Address(email="mailtrap@example.com",
        #                       name="Mailtrap Test"),
        #     to=[mt.Address(email="khoi.kioto@gmail.com")],
        #     subject="You are awesome!",
        #     text="Congrats for sending test email with Mailtrap!",
        # )

        # # create client and send
        # client = mt.MailtrapClient(token="8a9fb48cf48667640dc469dfb0ccde58")
        # client.send(mail)
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
        qr.read(id=id)
        return {'message': 'No Content'}, 200
