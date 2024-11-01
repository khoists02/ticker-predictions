# Prediction System power by Khoi.le
from flask import Flask, current_app
from flask_restful import Api, abort
from resources.api.predicts import StockData, StockDataDaily
from webargs.flaskparser import parser
from resources.database import db
from resources.config import AppConfig
from flask_cors import CORS
from flask_mail import Mail
import datetime
import pytz
# from flask_socketio import SocketIO, emit, send
# set configuration values

VN_TZ = pytz.timezone("Asia/Ho_Chi_Minh")


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
mail = mail_app
api = Api(app)

# Routes APIs
api.add_resource(StockData, '/api/v1/data')
api.add_resource(StockDataDaily, '/api/v1/daily')

# socketio = SocketIO(app)

@parser.error_handler
def handle_request_parsing_error(err, req, schema, *, error_status_code, error_headers):
    abort(error_status_code, errors=err.messages)


def print_date():
    date_now = datetime.datetime.now(VN_TZ)
    date_time_fm = date_now.strftime('%Y-%m-%d %H:%M')

    print(date_time_fm)

with app.app_context():
    print("======= Database start... ======")
    # Database Config
    db.init_app(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
