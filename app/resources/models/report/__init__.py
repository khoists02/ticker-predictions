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

    def create(self, ticker, increase, decrease, date) -> None:
        data = Report(ticker=ticker, increase=increase, decrease=decrease,
                      date=date,)
        db.session.add(data)
        db.session.commit()
