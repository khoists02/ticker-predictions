from sqlalchemy import Column, UUID, String, Boolean, Float, text
from resources.database import db


class Sessions(db.Model):
    __tablename__ = "sessions"
    id = Column(UUID, primary_key=True,
                server_default=text("uuid_generate_v4()"),)
    ticker = Column(String, nullable=False)
    current_price = Column(Float, nullable=False)
    previous_price = Column(Float, nullable=False)
    date = Column(String, nullable=False)
    date_time = Column(String, nullable=False)

    def __repr__(self):
        return '<Sessions %r>' % self.serialize

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': str(self.id),
            'ticker': self.ticker,
            'current_price': self.current_price,
            'previous_price': self.previous_price,
            'date': self.date,
            'date_time': self.date_time,
        }


class SessionsQuery:
    def __init__(self) -> None:
        pass

    def count(self, ticker, current, previous, date) -> int:
        rs = db.session.query(Sessions) \
            .filter(
                Sessions.ticker == ticker,
                Sessions.current_price == current,
                Sessions.previous_price == previous,
                Sessions.date == date
        )

        return len(list(rs))

    def create(self, ticker, current, previous, date, date_time) -> None:
        data = Sessions(ticker=ticker, current_price=current, previous_price=previous,
                        date=date, date_time=date_time)
        db.session.add(data)
        db.session.commit()

    def delete_sessions(self, ticker: str, date: str):
        rs = db.session.query(Sessions) \
            .filter(
                Sessions.ticker == ticker,
                Sessions.date == date,
        )

        count = len(list(rs))
        if count > 0:
            for session in rs:
                db.session.delete(session)
                db.session.commit()
