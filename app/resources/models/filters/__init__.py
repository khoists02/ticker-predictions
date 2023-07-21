from sqlalchemy import Column, UUID, String, Integer, Float, Boolean
from resources.database import db
from resources.models.ticker_details import TickerDetails, TickerDetailsQuery


class Filters(db.Model):
    __tablename__ = "filters"
    id = Column(UUID, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    steps = Column(Integer, nullable=False)
    scale = Column(Boolean, nullable=False)
    split_by_date = Column(String, nullable=False)
    cols = Column(Boolean, nullable=False)
    test_size = Column(Float, nullable=False)
    shuffle = Column(Boolean, nullable=False)
    look_step = Column(Integer, nullable=False)
    n_steps = Column(Integer, nullable=False)
    epochs = Column(Integer, nullable=False)
    batch_size = Column(Integer, nullable=False)
    units = Column(Integer, nullable=False)
    ticker_id = Column(UUID, nullable=False)
    user_id = Column(UUID, nullable=False)
    # # Optional Mapping
    # ticker_details = db.relationship('TickerDetails', foreign_keys=ticker_id)

    def __repr__(self):
        return '<Filters %r>' % self.serialize

    def load_ticker_details(self) -> TickerDetails:
        return TickerDetailsQuery().findOneById(self.ticker_id)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': str(self.id),
            'name': self.name,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date),
            'steps': self.steps,
            'scale': self.scale,
            'split_by_date': self.split_by_date,
            'cols': self.cols,
            'test_size': self.test_size,
            'shuffle': self.shuffle,
            'look_step': self.look_step,
            'n_steps': self.n_steps,
            'epochs': self.epochs,
            'batch_size': self.batch_size,
            'units': self.units,
            'ticker_id': str(self.ticker_id),
            'user_id': str(self.user_id),
            'ticker': self.load_ticker_details().ticker,
        }


class FiltersQuery:
    def __init__(self) -> None:
        pass

    def findOneById(self, id) -> Filters:
        return db.session.query(Filters) \
            .filter(Filters.id == id) \
            .first()

    def findAll(self):
        result = db.session.query(Filters)
        return result
