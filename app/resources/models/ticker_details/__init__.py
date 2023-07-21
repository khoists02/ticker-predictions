from sqlalchemy import Column, UUID, String, Boolean, Double, Integer, PrimaryKeyConstraint
from resources.database import db


class TickerDetails(db.Model):
    __tablename__ = "ticker_details"
    id = Column(UUID, primary_key=True)
    ticker = Column(String, nullable=False)
    name = Column(String, nullable=False)
    market = Column(String, nullable=True)
    locale = Column(String, nullable=True)
    primary_exchange = Column(String, nullable=True)
    type = Column(String, nullable=True)
    active = Column(Boolean, nullable=True)
    currency_name = Column(String, nullable=True)
    cik = Column(String, nullable=True)
    address = Column(String, nullable=True)
    description = Column(String, nullable=True)
    market_cap = Column(Double, nullable=True)
    composite_figi = Column(String, nullable=True)
    share_class_figi = Column(String, nullable=True)
    sic_code = Column(String, nullable=True)
    sic_description = Column(String, nullable=True)
    total_employees = Column(Double, nullable=True)
    branding = Column(String, nullable=True)
    share_class_shares_outstanding = Column(Double, nullable=True)
    weighted_shares_outstanding = Column(Double, nullable=True)
    round_lot = Column(Integer, nullable=True)

    def __repr__(self):
        return '<TickerDetails %r>' % self.serialize

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': str(self.id),
            'ticker': self.ticker
        }


class TickerDetailsQuery:
    def __init__(self) -> None:
        pass

    def findOneById(self, id) -> TickerDetails:
        return db.session.query(TickerDetails).filter(
            TickerDetails.id == id).first()
