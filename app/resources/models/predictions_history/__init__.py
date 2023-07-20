from sqlalchemy import Column, UUID, String
from resources.database import db

class PredictionsHistory(db.Model):
    id = Column(UUID, primary_key=True)
    loss = Column(String, nullable=True)
    future_price = Column(String, nullable=True)
    accuracy_score = Column(String, nullable=True)
    total_buy_profit = Column(String, nullable=True)
    total_sell_profit = Column(String, nullable=True)
    total_profit = Column(String, nullable=True)
    profit_per_trade = Column(String, nullable=True)
    filter_id = Column(UUID, nullable=False)
    user_id = Column(UUID, nullable=False)

    def __repr__(self):
        return '<PredictionsHistory %r>' % self.filter_id
    
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
          'id': self.id,
          'loss': self.loss,
          'future_price': self.future_price,
          'accuracy_score': self.accuracy_score,
          'total_buy_profit': self.total_buy_profit,
          'total_sell_profit': self.total_sell_profit,
          'total_profit': self.total_profit,
          'profit_per_trade': self.profit_per_trade,
          'filter_id': self.filter_id,
          'user_id': self.user_id
       }
    
class PredictionsHistoryQuery:
    def __init__(self) -> None:
        pass

    def findOneById(self, id) -> PredictionsHistory:
        return db.session.query(PredictionsHistory).filter(
            PredictionsHistory.id == id).first()

    def findAll(self):
        result = db.session.query(PredictionsHistory)
        return result