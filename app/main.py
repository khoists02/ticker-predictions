from flask import Flask
from flask_restful import Api, abort
from resources.api.predicts import Predict, StockData, StockInfo, StockCashFlowSheet, StockDataDaily
from resources.api.prediction_history import PredictionsHistory
from resources.api.tickers_account import TickersAccount, TickerSettings
from resources.api.favorite_controller import FavoriteController
from resources.api.notification_controller import NotificationController, NotificationDetails, NotificationCount
from webargs.flaskparser import parser
from resources.database import db
from resources.config import AppConfig
from flask_cors import CORS, cross_origin

appConfig = AppConfig()


app = Flask(__name__)
CORS(app, origins="http://localhost:3002", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True)
api = Api(app)

# Database Config
app.config["SQLALCHEMY_DATABASE_URI"] = appConfig.SQLALCHEMY_DATABASE_URI
db.init_app(app)

# Routers
api.add_resource(Predict, '/api/v1/predict')
api.add_resource(PredictionsHistory, '/api/v1/history')
api.add_resource(StockData, '/api/v1/data')
api.add_resource(StockDataDaily, '/api/v1/daily')
api.add_resource(StockCashFlowSheet, '/api/v1/cashflow')
api.add_resource(TickersAccount, '/api/v1/account')
api.add_resource(StockInfo, '/api/v1/info')
api.add_resource(TickerSettings, '/api/v1/settings')
api.add_resource(FavoriteController, '/api/v1/favorites')

# Notification
api.add_resource(NotificationController, '/api/v1/notifications')
api.add_resource(NotificationCount, '/api/v1/notifications/count')
api.add_resource(NotificationDetails,
                 '/api/v1/notifications/<uuid:id>/read')
# api.add_resource(StockData, '/api/v1/balancesheet')


@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    abort(error_status_code, errors=err.messages)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
