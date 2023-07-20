from sqlalchemy import Column, UUID, String, Integer, Float, Boolean
from database import db

class Filter(db.Model):
    id = Column(UUID, primary_key=True)
    steps = Column(Integer, nullable=False)
    scale = Column(Boolean, nullable=False)
    split_by_date = Column(String, nullable=False)
    cols = Column(Boolean, nullable=False)
    test_size = Column(Float, nullable=False)
    shuffle = Column(Boolean, nullable=False)
    look_step = Column(Boolean, nullable=False)
    n_steps = Column(Integer, nullable=False)
    epochs = Column(Integer, nullable=False)
    batch_size = Column(Integer, nullable=False)
    units = Column(Integer, nullable=False)
    ticker_id = Column(UUID, nullable=False)
    user_id = Column(UUID, nullable=False)

    def __repr__(self):
        return '<PredictionsHistory %r>' % self.ticker_id