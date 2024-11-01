from yfinance import AssertionError
from webargs import fields
from webargs.flaskparser import use_kwargs

class Predict(Resource):
    def __init__(self):
       pass

    get_args = {
        'id': fields.Str(
            required=True
        )
    }
    post_args = {
        'filter_id': fields.Str(
            required=True
        )
    }
