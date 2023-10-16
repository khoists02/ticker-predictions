from sqlalchemy import Column, UUID, String, Float, update
from resources.database import db


class Settings(db.Model):
    id = Column(UUID, primary_key=True)
    ticker = Column(String, nullable=False)
    balance = Column(Float, nullable=True)
    current = Column(Float, nullable=True)
    count = Column(Float, nullable=False)
    price_in = Column(Float, nullable=False, default=0)


class SettingQuery:
    def findByTicker(self, ticker) -> Settings:
        return db.session.query(Settings).filter(
            Settings.ticker == ticker).first()

    def updateSetting(self, id, balance, current, count, priceIn) -> None:
        st: Settings = db.session.query(Settings).filter(
            Settings.id == id).first()
        st.balance = balance
        st.current = current
        st.count = count
        st.price_in = priceIn
        db.session.commit()
