from flask import Flask, current_app
from flask_restful import Api, abort
from resources.api.predicts import StockData, StockInfo, StockCashFlowSheet, StockDataDaily, StockBalanceSheet, StockRecommendations
from resources.api.bidasks import BidAskController, BidAsksDetails
from resources.api.tickers_account import TickersAccount, TickerSettings
from resources.api.prediction_history import TickerEarningDates
from resources.api.favorite_controller import FavoriteController
from resources.api.notification_controller import NotificationController, NotificationDetails, NotificationCount
from resources.api.report import ReportController, ReportByDateController
from resources.api.plays_controller import PlayDetailsController, PlaysController
from resources.api.tickers import TickerFastInfoController
from webargs.flaskparser import parser
from resources.database import db
from resources.config import AppConfig
from flask_cors import CORS
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from resources.jobs import Job
import datetime
import pytz
from flask_socketio import SocketIO, emit, send
# set configuration values

VN_TZ = pytz.timezone("Asia/Ho_Chi_Minh")


class Config:
    SCHEDULER_API_ENABLED = True


appConfig = AppConfig()
app = Flask(__name__, template_folder='templates')

# log config
# logging.basicConfig(filename='record-{}.log'.format(datetime.datetime.now(tz=VN_TZ).strftime('%Y-%m-%d %H:%M')), level=logging.DEBUG,
#                     format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

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
# db.init_app(app)

# routes APIs
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
api.add_resource(BidAsksDetails,
                 '/api/v1/bidasks/<uuid:id>')
api.add_resource(TickerEarningDates, '/api/v1/earningdates')

api.add_resource(PlayDetailsController,
                 '/api/v1/plays/<uuid:id>')
api.add_resource(PlaysController, '/api/v1/plays')

# Notification
api.add_resource(NotificationController, '/api/v1/notifications')
api.add_resource(NotificationCount, '/api/v1/notifications/count')
api.add_resource(NotificationDetails,
                 '/api/v1/notifications/<uuid:id>/read')
# Report
api.add_resource(ReportController, '/api/v1/report')
api.add_resource(ReportByDateController, '/api/v1/reportfilter')
# api.add_resource(StockData, '/api/v1/balancesheet')

# Tickers Info
api.add_resource(TickerFastInfoController, '/api/v1/short')

socketio = SocketIO(app)


@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    abort(error_status_code, errors=err.messages)


def print_date():
    date_now = datetime.datetime.now(VN_TZ)
    date_time_fm = date_now.strftime('%Y-%m-%d %H:%M')

    print(date_time_fm)


# def test(data):
#     part = data.split("@")
#     rs = ":".join(part[::-1])
#     return rs


# data = [
#     "user112204:t2hxuw@108.165.167.70:8988",
#     "user112204:t2hxuw@108.165.167.71:8988",
#     "user112204:t2hxuw@108.165.167.141:8988",
#     "user112204:t2hxuw@108.165.167.78:8988",
#     "user112204:t2hxuw@108.165.167.75:8988",
#     "user112204:t2hxuw@108.165.167.173:8988",
#     "user112204:t2hxuw@163.5.88.136:8988",
#     "user112204:t2hxuw@108.165.167.37:5594",
#     "user112204:t2hxuw@108.165.167.140:5594",
#     "user112204:t2hxuw@108.165.167.107:5594",
#     "user112204:t2hxuw@108.165.167.31:5594",
#     "user112204:t2hxuw@108.165.167.200:5594",
#     "user112204:t2hxuw@108.165.167.221:5594",
#     "user112204:t2hxuw@108.165.167.234:5594",
#     "user112204:t2hxuw@108.165.167.36:5594",
#     "user112204:t2hxuw@108.165.167.219:5594",
#     "user112204:t2hxuw@108.165.167.223:5594",
#     "user112204:t2hxuw@195.96.157.160:3730",
#     "user112204:t2hxuw@195.96.157.241:3730",
#     "user112204:t2hxuw@195.96.157.127:3730",
#     "user112204:t2hxuw@195.96.157.17:3730",
#     "user112204:t2hxuw@195.96.157.64:3730",
#     "user112204:t2hxuw@45.15.252.199:1193",
#     "user112204:t2hxuw@45.15.252.234:1193",
#     " user112204:t2hxuw@45.15.252.89:1193 ",
#     " user112204:t2hxuw@45.15.252.241:1193 ",
#     "user112204:t2hxuw@45.15.252.96:1193",
#     "user112204:t2hxuw@45.15.252.26:1193 ",
#     "user112204:t2hxuw@45.15.252.173:1193",
#     "user112204:t2hxuw@45.15.252.94:1193",
#     "user112204:t2hxuw@45.15.252.247:1193 ",
#     "user112204:t2hxuw@45.15.252.188:1193",
#     "user112204:t2hxuw@45.15.252.8:1193 ",
#     "user112204:t2hxuw@45.15.252.202:1193 ",
#     "user112204:t2hxuw@45.15.252.125:1193",
#     "user112204:t2hxuw@45.15.252.136:1193",
#     "user112204:t2hxuw@45.15.252.237:1193",
#     "user112204:t2hxuw@45.15.252.128:2629",
#     "user112204:t2hxuw@45.15.252.194:2629",
#     "user112204:t2hxuw@45.15.252.120:2629",
#     "user112204:t2hxuw@45.15.252.98:2629",
#     "user112204:t2hxuw@45.15.252.197:2629",
#     "user112204:t2hxuw@45.15.252.143:2629",
#     "user112204:t2hxuw@45.15.252.170:2629",
#     "user112204:t2hxuw@45.15.252.67:2629",
#     "user112204:t2hxuw@45.15.252.107:2422",
#     "user112204:t2hxuw@45.15.252.41:2422",
#     "user112204:t2hxuw@45.15.252.244:1799",
#     "user112204:t2hxuw@45.15.252.182:5777",
#     "user112204:t2hxuw@185.251.22.60:3631"
# ]

# for i in data:

#     print(test(i))

with app.app_context():
    print("======= Database start... ======")
    # Database Config
    db.init_app(app)
    print("======= Job Context ======")

    scheduler = BackgroundScheduler()

    scheduler.configure(timezone=VN_TZ)

    print("==== Add job store ====")
    # scheduler.add_jobstore('sqlalchemy', engine=db.engine)

    print("==== Add main jobs ====")

    # defined jobs
    # def job_delete_session():
    #     print("========  Start delete session Job ========")

    #     with app.app_context():
    #         new_job = Job(ticker="BLND")
    #         new_job.delete_sessions()

    #     print("========  End delete session Job ========")

    def job_pm():
        print("========  Start import data Job at PM ========")
        print_date()
        with app.app_context():
            new_job = Job(ticker="BLND")
            new_job.import_session_data()

        print("========  End import data Job at PM ========")

    def job_am():

        print("========  Start import data Job at AM ========")
        print_date()
        with app.app_context():
            new_job = Job(ticker="BLND")
            new_job.import_session_data()

        print("========  End import data Job at AM ========")

    def job_report():
        print("========  Start report Job ========")
        print_date()
        with app.app_context():
            new_job = Job(ticker="BLND")
            new_job.count_sessions()

        print("========  End report Job ========")

    def job_report_today():
        print("========  Start report today Job ========")
        print_date()
        with app.app_context():
            new_job = Job(ticker="BLND")
            new_job.count_sessions_today()

        print("========  End report today Job ========")

    def job_tracking():
        print("==== Tracking ====")
        print_date()

    # Import data 20-23 *5
    # Schedule the cron job to run every 5mn from 0AM - 23PM every working day
    scheduler.add_job(
        func=job_pm,
        trigger='cron', day_of_week='mon-fri', hour='20-23', minute='*/5'  # 20PM-23PM
    )

    # 05-5 *5
    # Schedule the cron job to run on Saturday from 00 AM - 5AM every 5mn
    scheduler.add_job(
        func=job_am,
        trigger='cron', day_of_week='mon-sat', hour='0-5', minute='*/5'  # 0AM - 5AM
    )

    # TODO: Report today 7AM
    scheduler.add_job(
        func=job_report,
        trigger='cron', day_of_week='mon-sat', hour=7
    )

    # TODO: Report Today at 8AM
    scheduler.add_job(
        func=job_report_today,
        trigger='cron', day_of_week='mon-sat', hour=8
    )

    scheduler.add_job(
        func=job_tracking,
        trigger='cron', hour='*'
    )

    # TODO: 7AM
    # scheduler.add_job(
    #     func=job_delete_session,
    #     trigger='cron', day_of_week='mon-sat', hour=7  # Run 6AM every mon-sat
    # )

    print("==== Start scheduler ====")
    # Start the scheduler
    scheduler.start()

    print("Scheduled time zone {}".format(scheduler.timezone))

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())

    # TODO: Run manually
    # new_job = Job(ticker="BLND")
    # new_job.count_sessions_today()

    # logging.log(msg='Start scheduler configuration', level=logging.INFO)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
