from sqlalchemy import Column, UUID, String, Float, Boolean
from resources.database import db
import sqlalchemy


class Notification(db.Model):
    __tablename__ = "notifications"
    id = Column(UUID, primary_key=True,
                server_default=sqlalchemy.text("uuid_generate_v4()"),)
    ticker = Column(String, nullable=False)
    per = Column(Float, nullable=False, default=0)
    close = Column(Float, nullable=False, default=0)
    updatedAt = Column(String, nullable=True)
    read = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return '<Notification %r>' % self.serialize

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': str(self.id),
            'ticker': self.ticker,
            'per': self.per,
            'close': self.close,
            'updatedAt': self.updatedAt,
            'read': self.read
        }


class NotificationQuery:
    def __init__(self) -> None:
        pass

    def findAll(self):
        rs = db.session.query(Notification)
        return rs

    def createOne(self, body):
        data = Notification(per=body['per'], read=False, ticker=body['ticker'],
                            updatedAt=body['updatedAt'], close=body['close'])
        db.session.add(data)
        db.session.commit()

    def read(self, id):
        nt: Notification = db.session.query(Notification).filter(
            Notification.id == id).first()
        nt.read = True
        db.session.commit()

    def count(self):
        rs = db.session.query(Notification).filter(
            Notification.read == False)
        return len(list(rs))
