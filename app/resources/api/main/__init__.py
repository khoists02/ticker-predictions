from flask_restful import Resource
from flask import jsonify
import numpy as np
import pandas as pd
import random
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Bidirectional
from keras.callbacks import ModelCheckpoint, TensorBoard
import time
from resources.helpers import Helpers

class Main(Resource):
    def __init__(self):
        self.helper = Helpers()
        # set seed, so we can get the same results after rerunning several times
        np.random.seed(314)
        tf.random.set_seed(314)
        random.seed(314)
        
        # Window size or the sequence length
        self.N_STEPS = 50
        # Lookup step, 1 is the next day
        self.LOOKUP_STEP = 15
        # whether to scale feature columns & output price as well
        self.SCALE = True
        self.scale_str = f"sc-{int(self.SCALE)}"
        # whether to shuffle the dataset
        self.SHUFFLE = True
        self.shuffle_str = f"sh-{int(self.SHUFFLE)}"
        # whether to split the training/testing set by date
        self.SPLIT_BY_DATE = False
        self.split_by_date_str = f"sbd-{int(self.SPLIT_BY_DATE)}"
        # test ratio size, 0.2 is 20%
        self.TEST_SIZE = 0.2
        # features to use
        self.FEATURE_COLUMNS = ["adjclose", "volume", "open", "high", "low"]
        # date now
        self.date_now = time.strftime("%Y-%m-%d")
        ### model parameters
        self.N_LAYERS = 2
        # LSTM cell
        self.CELL = LSTM
        # 256 LSTM neurons
        self.UNITS = 256
        # 40% dropout
        self.DROPOUT = 0.4
        # whether to use bidirectional RNNs
        self.BIDIRECTIONAL = False
        ### training parameters
        # mean absolute error loss
        # LOSS = "mae"
        # huber loss
        self.LOSS = "huber_loss"
        self.OPTIMIZER = "adam"
        self.BATCH_SIZE = 64
        self.EPOCHS = 50
        # Amazon stock market
        self.ticker = "AMZN"


    def get(self):
        data = self.helper.load_stock_data(self.ticker, self.N_STEPS, scale=self.SCALE, split_by_date=self.SPLIT_BY_DATE,
                shuffle=self.SHUFFLE, lookup_step=self.LOOKUP_STEP, test_size=self.TEST_SIZE,
                feature_columns=self.FEATURE_COLUMNS)
        model = self.create_model(
            sequence_length=self.N_STEPS,
            n_features=len(self.FEATURE_COLUMNS),
            units=self.UNITS,
            cell=self.CELL,
            n_layers=self.N_LAYERS,
            dropout=self.DROPOUT,
            loss=self.LOSS,
            optimizer=self.OPTIMIZER,
            bidirectional=self.BIDIRECTIONAL
        )
        history = model.fit(data["X_train"], data["y_train"],
                    batch_size=self.BATCH_SIZE,
                    epochs=self.EPOCHS,
                    validation_data=(data["X_test"], data["y_test"]),
                    verbose=1)
        future_price = self.predict(model, data)
        print(f"Future price after {self.LOOKUP_STEP} days is {future_price:.2f}$")
        return jsonify({'price': f"Future price after {self.LOOKUP_STEP} days is {future_price:.2f}$"})
    
    def create_model(self, sequence_length, n_features, units=256, cell=LSTM, n_layers=2, dropout=0.3,
                loss="mean_absolute_error", optimizer="rmsprop", bidirectional=False):
      model = Sequential()
      print("access_function")
      for i in range(n_layers):
          if i == 0:
              # first layer
              if bidirectional:
                  model.add(Bidirectional(cell(units, return_sequences=True), batch_input_shape=(None, sequence_length, n_features)))
              else:
                  model.add(cell(units, return_sequences=True, batch_input_shape=(None, sequence_length, n_features)))
          elif i == n_layers - 1:
              # last layer
              if bidirectional:
                  model.add(Bidirectional(cell(units, return_sequences=False)))
              else:
                  model.add(cell(units, return_sequences=False))
          else:
              # hidden layers
              if bidirectional:
                  model.add(Bidirectional(cell(units, return_sequences=True)))
              else:
                  model.add(cell(units, return_sequences=True))
          # add dropout after each layer
          model.add(Dropout(dropout))
      model.add(Dense(1, activation="linear"))
      model.compile(loss=loss, metrics=["mean_absolute_error"], optimizer=optimizer)
      return model
    
    def predict(self,model, data):
      # retrieve the last sequence from data
      last_sequence = data["last_sequence"][-self.N_STEPS:]
      # expand dimension
      last_sequence = np.expand_dims(last_sequence, axis=0)
      # get the prediction (scaled from 0 to 1)
      prediction = model.predict(last_sequence)
      # get the price (by inverting the scaling)
      if self.SCALE:
          predicted_price = data["column_scaler"]["adjclose"].inverse_transform(prediction)[0][0]
      else:
          predicted_price = prediction[0][0]
      return predicted_price
    
