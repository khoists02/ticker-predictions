from flask import Flask, jsonify
from flask_restful import Api
from resources.api.main import Main


app = Flask(__name__)
api = Api(app)

api.add_resource(Main, '/api/v1/main')

if __name__ == '__main__':
  app.run()