from sqlalchemy import Column, UUID, String, Float, text
from resources.database import db


class Report(db.Model):
    __tablename__ = "report"
    id = Column(UUID, primary_key=True,
                server_default=text("uuid_generate_v4()"),)
    ticker = Column(String, nullable=False)
    increase = Column(Float, nullable=False)
    decrease = Column(Float, nullable=False)
    date = Column(String, nullable=False)

    def __repr__(self):
        return '<Report %r>' % self.serialize

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': str(self.id),
            'ticker': self.ticker,
            'increase': self.current_price,
            'decrease': self.previous_price,
            'date': self.date,
        }


class ReportQuery:
    def __init__(self) -> None:
        pass

    def find_all(self):
        rs = db.session.query(Report)
        return [i.serialize for i in rs]

    def find_all_by_date(self, date: str):
        rs = db.session.query(Report) \
            .filter(Report.date == date)
        return [i.serialize for i in rs]

    def create(self, ticker, increase, decrease, date) -> None:
        data = Report(ticker=ticker, increase=increase, decrease=decrease,
                      date=date,)
        db.session.add(data)
        db.session.commit()
