from flask import Flask
from flask_restful import Api, abort
from resources.api.predicts import StockData, StockInfo, StockCashFlowSheet, StockDataDaily, StockBalanceSheet, StockRecommendations
from resources.api.bidasks import BidAskController
from resources.api.tickers_account import TickersAccount, TickerSettings
from resources.api.prediction_history import TickerEarningDates
from resources.api.favorite_controller import FavoriteController
from resources.api.notification_controller import NotificationController, NotificationDetails, NotificationCount
from webargs.flaskparser import parser
from resources.database import db
from resources.config import AppConfig
from flask_cors import CORS
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import time


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True


appConfig = AppConfig()
app = Flask(__name__, template_folder='templates')
mail_app = Mail(app=app)

origins = ["https://localhost:3000", "http://localhost:3002",
           "http://localhost:3000", "https://volvo.local:3000"]

CORS(app, origins=origins, allow_headers=[
    "Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True)
app.config['MAIL_SERVER'] = 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '75484011e5c514'
app.config['MAIL_PASSWORD'] = 'b82e5a6b2d862e'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = appConfig.SQLALCHEMY_DATABASE_URI
app.config["SCHEDULER_API_ENABLED"] = True
mail_app = Mail(app=app)
mail = mail_app
api = Api(app)

# Database Config
db.init_app(app)

# Routers
# api.add_resource(Predict, '/api/v1/predict')
# api.add_resource(PredictionsHistory, '/api/v1/history')
api.add_resource(StockData, '/api/v1/data')
api.add_resource(StockDataDaily, '/api/v1/daily')
api.add_resource(StockCashFlowSheet, '/api/v1/cashflow')
api.add_resource(StockBalanceSheet, '/api/v1/balanceSheet')
api.add_resource(StockRecommendations, '/api/v1/recommendations')
api.add_resource(TickersAccount, '/api/v1/account')
api.add_resource(StockInfo, '/api/v1/info')
api.add_resource(TickerSettings, '/api/v1/settings')
api.add_resource(FavoriteController, '/api/v1/favorites')
api.add_resource(BidAskController, '/api/v1/bidasks')
api.add_resource(TickerEarningDates, '/api/v1/earningdates')

# Notification
api.add_resource(NotificationController, '/api/v1/notifications')
api.add_resource(NotificationCount, '/api/v1/notifications/count')
api.add_resource(NotificationDetails,
                 '/api/v1/notifications/<uuid:id>/read')
# api.add_resource(StockData, '/api/v1/balancesheet')


@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    abort(error_status_code, errors=err.messages)


scheduler = BackgroundScheduler()


def my_cron_job():
    # Code to be executed by the cron job
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


# Schedule the cron job to run every 1mn
scheduler.add_job(
    func=my_cron_job,
    trigger="interval", seconds=60,
)

# Start the scheduler
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
