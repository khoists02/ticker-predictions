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
from flask_cors import CORS
from flask_mail import Mail, Message

appConfig = AppConfig()
app = Flask(__name__)
mail = Mail(app=app)
CORS(app, origins="http://localhost:3002", allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True)
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '75484011e5c514'
app.config['MAIL_PASSWORD'] = 'b82e5a6b2d862e'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = appConfig.SQLALCHEMY_DATABASE_URI
mail = Mail(app=app)
api = Api(app)

# Database Config
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


@app.route("/")
def index():
    msg = Message('Hello from the other side!',
                  sender='peter@mailtrap.io', recipients=['paul@mailtrap.io'])
    msg.body = "Hey Paul, sending you this email from my Flask app, lmk if it works"
    mail.send(msg)
    return "Message sent!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
