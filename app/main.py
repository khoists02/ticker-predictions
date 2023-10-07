from flask import Flask
from flask_restful import Api, abort
from resources.api.predicts import Predict, StockData, StockBalanceSheet, StockCashFlowSheet
from resources.api.prediction_history import PredictionsHistory
from webargs.flaskparser import parser
from resources.database import db
from resources.config import AppConfig

appConfig = AppConfig()


app = Flask(__name__)
api = Api(app)

# Database Config
app.config["SQLALCHEMY_DATABASE_URI"] = appConfig.SQLALCHEMY_DATABASE_URI
db.init_app(app)

# Routers
api.add_resource(Predict, '/api/v1/predict')
api.add_resource(PredictionsHistory, '/api/v1/history')
api.add_resource(StockData, '/api/v1/data')
api.add_resource(StockCashFlowSheet, '/api/v1/cashflow')
# api.add_resource(StockData, '/api/v1/balancesheet')


@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    abort(error_status_code, errors=err.messages)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
