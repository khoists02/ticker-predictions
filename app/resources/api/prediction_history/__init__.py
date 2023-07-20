from flask_restful import Resource
from flask import jsonify
from resources.models.predictions_history import PredictionsHistoryQuery
import json

class PredictionsHistory(Resource):
    def __init__(self):
      self.model = PredictionsHistoryQuery()
  
    def get(self): # Find all
        return [i.serialize for i in self.model.findAll()], 200
