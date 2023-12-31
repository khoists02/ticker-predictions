from resources.helpers import Helpers
from resources.models.sessions import SessionsQuery
from resources.models.report import ReportQuery
from resources.models.notification import NotificationQuery
from resources.api.settings import SettingQuery
import datetime
from sqlalchemy import text
from resources.database import db
import pytz
import json
from resources.services.send_mail import SendMailStockService

# import logging
# import datetime
# import pytz
# set configuration values


class Job:
    def __init__(self, ticker: str) -> None:
        # log config
        tz_VN = pytz.timezone('Asia/Ho_Chi_Minh')
        # logging.basicConfig(filename='job-{}.log'.format(datetime.datetime.now(tz=tz_VN).strftime('%Y-%m-%d %H:%M')), level=logging.DEBUG,
        #                     format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
        date_now = datetime.datetime.now(tz_VN)
        date_now_fm = date_now.strftime('%Y-%m-%d')
        date_time_fm = date_now.strftime('%Y-%m-%d %H:%M')
        # 2023-10-19
        # 2023-10-19 01:41
        self.helper = Helpers()
        self.query = SessionsQuery()
        self.report_query = ReportQuery()
        self.setting_qr = SettingQuery()
        self.ticker = ticker
        self.date = date_now_fm
        self.current_date = date_now.strptime(date_now_fm, '%Y-%m-%d')
        self.date_time = date_time_fm
        self.notification_qr = NotificationQuery()

    def import_session_data(self) -> None:
        # TODO: replace when ticker info back
        rs = json.loads(self.helper.get_ticker_fast_info(ticker=self.ticker))

        if rs is not None:
            prev = rs['regularMarketPreviousClose']
            current = rs['lastPrice']

            # rs['currentPrice'] = rs['lastPrice']
            # rs['previousClose'] = rs['regularMarketPreviousClose']
            # check exist data here
            count = self.query.count(
                ticker=self.ticker, current=current, previous=prev, date=self.date)
            if count > 0:
                return None
            else:
                # logging.log(msg='Start scheduler configuration',
                #             level=logging.WARNING)
                try:
                    self.query.create(ticker=self.ticker, current=current,
                                      previous=prev, date=self.date, date_time=self.date_time)
                    setting = self.setting_qr.findByTicker(ticker="BLND")
                    print("Price Should Buy {}".format(setting['priceIn']))

                    if setting['priceIn'] > current:
                        print("Send notification and email !!!")
                        body = {
                            'per': ((current - prev) / current) * 100,
                            'read': False,
                            'ticker': 'BLND',
                            'updatedAt': self.date,
                            'close': current,
                        }
                        self.notification_qr.createOne(body=body)
                        email_service = SendMailStockService()
                        txt = 'increase' if float(
                            body['per']) > 0 else 'decrease'
                        email_service.send_email(
                            txt=txt,
                            username='khoi.le', link='http://localhost:3002/histories/BLND', ticker=body['ticker'], per=body['per'], close=body['close'], updatedAt=body['updatedAt'])
                except:
                    print("Unique")

    def delete_sessions(self) -> None:
        self.query.delete_sessions(ticker=self.ticker, date=self.date)

    """
        find all data from yesterday
    """

    def count_sessions(self):
        count_increase = 0
        count_decrease = 0
        yesterday = self.current_date + datetime.timedelta(days=-1)
        str_date = yesterday.strftime('%Y-%m-%d')  # format datetime yesterday
        rs = self.query.find_all_sessions_by_current_date(
            ticker=self.ticker, date=str_date)
        if len(rs) > 0:
            for index, item in enumerate(rs):
                first_item = rs[0]  # TODO: get first item
                if index == 0:
                    continue
                if item['current_price'] > first_item['current_price']:
                    count_increase = count_increase + 1
                elif item['current_price'] == first_item['current_price']:
                    print("Equal")
                else:
                    count_decrease = count_decrease + 1

        print("count increase {}".format(count_increase))
        print("count decrease {}".format(count_decrease))
        if count_decrease == 0 and count_increase == 0:
            return
        try:
            self.report_query.create(
                date=str_date, ticker="BLND", increase=count_increase, decrease=count_decrease)
        except:
            print("Unique")

    def count_sessions_today(self):
        count_increase = 0
        count_decrease = 0
        rs = self.query.find_all_sessions_by_current_date(
            ticker=self.ticker, date=self.date)
        if len(rs) > 0:
            for index, item in enumerate(rs):
                first_item = rs[0]  # TODO: get first item
                if index == 0:
                    continue
                if item['current_price'] > first_item['current_price']:
                    count_increase = count_increase + 1
                elif item['current_price'] == first_item['current_price']:
                    print("Equal")
                else:
                    count_decrease = count_decrease + 1

        print("count increase {}".format(count_increase))
        print("count decrease {}".format(count_decrease))
        if count_decrease == 0 and count_increase == 0:
            return
        try:
            self.report_query.create(
                date=self.date, ticker="BLND", increase=count_increase, decrease=count_decrease)
        except:
            print("Unique")
