from resources.helpers import Helpers
from resources.models.sessions import SessionsQuery
import datetime
from sqlalchemy import text
from resources.database import db
import pytz


class Job:
    def __init__(self, ticker: str) -> None:
        tz_VN = pytz.timezone('Asia/Ho_Chi_Minh')
        date_now = datetime.datetime.now(tz_VN)
        date_now_fm = date_now.strftime('%Y-%m-%d')
        date_time_fm = date_now.strftime('%Y-%m-%d %H:%M')
        # 2023-10-19
        # 2023-10-19 01:41
        self.helper = Helpers()
        self.query = SessionsQuery()
        self.ticker = ticker
        self.date = date_now_fm
        self.date_time = date_time_fm

    def import_session_data(self) -> None:
        rs = self.helper.get_ticker_daily(ticker=self.ticker)

        if rs is not None:
            prev = rs['previousClose']
            current = rs['currentPrice']

            # check exist data here
            count = self.query.count(
                ticker=self.ticker, current=current, previous=prev, date=self.date)
            print(count)
            if count > 0:
                return None
            else:
                self.query.create(ticker=self.ticker, current=current,
                                  previous=prev, date=self.date, date_time=self.date_time)

    def delete_sessions(self) -> None:
        self.query.delete_sessions(ticker=self.ticker, date=self.date)
