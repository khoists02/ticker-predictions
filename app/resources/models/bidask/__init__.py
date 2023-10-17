from sqlalchemy import Column, UUID, String, Float
from resources.database import db
import sqlalchemy


class BidAsk(db.Model):
    __tablename__ = "bid_asks"
    id = Column(UUID, primary_key=True,
                server_default=sqlalchemy.text("uuid_generate_v4()"),)
    ticker = Column(String, nullable=False)
    ask = Column(Float, nullable=False)
    bid = Column(Float, nullable=False)
    ask_size = Column(Float, nullable=False)
    bid_size = Column(Float, nullable=False)
    updated_at = Column(String, nullable=False)

    def __repr__(self):
        return '<BidAsk %r>' % self.serialize

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': str(self.id),
            'ticker': self.ticker,
            'bid': self.bid,
            'ask': self.ask,
            'bidSize': self.bid_size,
            'askSize': self.ask_size,
            'updatedAt': self.updated_at
        }


class BidAskQuery:
    def __init__(self) -> None:
        pass

    def findListByTicker(self, ticker):
        rs = db.session.query(BidAsk) \
            .filter(BidAsk.ticker == ticker)
        return rs

    def count(self, ticker, bid, ask, bid_size, ask_size) -> int:
        rs = db.session.query(BidAsk) \
            .filter(
                BidAsk.ticker == ticker,
                BidAsk.ask == ask,
                BidAsk.ask_size == ask_size,
                BidAsk.bid == bid,
                BidAsk.bid_size == bid_size
        )

        return len(list(rs))

    def create(self, ticker, bid, ask, bid_size, ask_size, updated_at) -> int:
        count = self.count(ticker=ticker, bid=bid, ask=ask,
                           bid_size=bid_size, ask_size=ask_size)

        if count > 0:
            return 0

        data = BidAsk(ticker=ticker, bid=bid, ask=ask,
                      bid_size=bid_size, ask_size=ask_size, updated_at=updated_at)
        db.session.add(data)
        db.session.commit()
        return 1
