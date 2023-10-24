from sqlalchemy import Column, UUID, String
from resources.database import db
import sqlalchemy


class Favorite(db.Model):
    __tablename__ = "favorites"
    id = Column(UUID, primary_key=True,
                server_default=sqlalchemy.text("uuid_generate_v4()"),)
    ticker = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    url_icon = Column(String, nullable=False)

    def __repr__(self):
        return '<Favorite %r>' % self.serialize

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': str(self.id),
            'ticker': self.ticker,
            'symbol': self.symbol,
            'url_icon': self.url_icon
        }


class FavoriteQuery:
    def __init__(self) -> None:
        pass

    def findListByTicker(self, ticker):
        rs = db.session.query(Favorite) \
            .filter(Favorite.ticker == ticker)
        print(rs)
        return rs

    def addNew(self, ticker):
        data = Favorite(ticker="BLND", symbol=ticker,
                        url_icon="https://google.com")
        db.session.add(data)
        db.session.commit()

    def delete(self, id: str):
        rs: Favorite = db.session.query(Favorite) \
            .filter(Favorite.id == id).first()
        db.session.delete(rs)

        db.session.commit()
