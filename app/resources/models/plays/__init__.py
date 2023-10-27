from sqlalchemy import Column, UUID, String, Float, Boolean, text, and_
from sqlalchemy.sql.expression import false
from resources.database import db


class Plays(db.Model):
    __tablename__ = "plays"
    id = Column(UUID, primary_key=True,
                server_default=text("uuid_generate_v4()"),)
    price = Column(Float, nullable=False, default=0)
    in_price = Column(Float, nullable=False, default=0)
    ticker = Column(String, nullable=False)
    virtual = Column(Boolean, nullable=True, default=False)
    played_at = Column(String, nullable=True)
    total = Column(Float, nullable=False)
    done = Column(Boolean, nullable=False)

    def __repr__(self):
        return '<Plays %r>' % self.serialize

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': str(self.id),
            'ticker': self.ticker,
            'price': self.price,
            'inPrice': self.in_price,
            'virtual': self.virtual,
            'playedAt': self.played_at,
            'total': self.total,
            'done': self.done
        }


class PlaysQuery:
    def __init__(self) -> None:
        pass

    def find_all(self):
        rs = db.session.query(Plays)
        return [i.serialize for i in rs]

    def find_all_by_ticker(self, ticker):
        rs = db.session.query(Plays) \
            .filter(and_(Plays.ticker == ticker, Plays.done.is_(False))).all()
        return [i.serialize for i in rs]

    def find_by_id(self, id: str):
        rs = db.session.query(Plays) \
            .filter(Plays.id == id).first()
        return rs.serialize

    def find_one(self, id):
        rs = db.session.query(Plays) \
            .filter(Plays.id == id).first()
        return rs

    def create(self, ticker, price, in_price, virtual, played_at, total, done) -> None:
        data = Plays(ticker=ticker, price=price, in_price=in_price, virtual=virtual,
                     played_at=played_at, total=total, done=done)
        db.session.add(data)
        db.session.commit()

    def update(self, id, ticker, price, in_price, virtual, played_at, total, done):
        play: Plays = self.find_one(id)
        print(play)
        play.ticker = ticker
        play.price = price
        play.in_price = in_price
        play.virtual = virtual
        play.played_at = played_at
        play.total = total
        play.done = done
        db.session.commit()

    def delete(self, id):
        play = self.find_one(id)
        db.session.delete(play)
        db.session.commit()
