from flask import Flask, jsonify
from flask_restful import Api, abort
from resources.api.main import Main
from webargs.flaskparser import parser


app = Flask(__name__)
api = Api(app)

api.add_resource(Main, '/api/v1/main')


@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    abort(error_status_code, errors=err.messages)


if __name__ == '__main__':
    app.run()
