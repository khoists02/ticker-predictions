from flask_restful import Resource
from flask import abort
from webargs import fields
from webargs.flaskparser import use_kwargs, use_args
from resources.models.report import ReportQuery


class ReportController(Resource):
    def __init__(self):
        pass

    # args = {
    #     'ticker': fields.Str(
    #         required=True
    #     ),
    # }

    def get(self):

        qr = ReportQuery()
        rs = qr.find_all()
        return {
            'content': rs
        }, 200


class ReportByDateController(Resource):
    def __init__(self) -> None:
        pass

    args = {
        'date': fields.Str(
            required=True
        ),
    }

    @use_kwargs(args, location='query')
    def get(self, date: str):
        qr = ReportQuery()
        rs = qr.find_all_by_date(date)
        return {
            'content': rs
        }, 200
