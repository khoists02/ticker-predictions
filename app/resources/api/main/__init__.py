from flask_restful import Resource, abort
from flask import jsonify
import numpy as np
import pandas as pd
import json
import random
import tensorflow as tf
from tensorflow.python.keras.layers import LSTM, Dense, Dropout
from tensorflow.python.keras.callbacks import ModelCheckpoint, TensorBoard
import time
from resources.helpers import Helpers
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser


class Main(Resource):
    def __init__(self):
        self.helper = Helpers()
        # set seed, so we can get the same results after rerunning several times
        np.random.seed(314)
        tf.random.set_seed(314)
        random.seed(314)

        # Window size or the sequence length
        self.N_STEPS = 50
        # whether to scale feature columns & output price as well
        # self.SCALE = True
        # self.scale_str = f"sc-{int(self.SCALE)}"

        # whether to split the training/testing set by date
        self.SPLIT_BY_DATE = False
        self.split_by_date_str = f"sbd-{int(self.SPLIT_BY_DATE)}"
        # features to use
        # date now
        self.date_now = time.strftime("%Y-%m-%d")
        # model parameters
        self.N_LAYERS = 2
        # LSTM cell
        self.CELL = LSTM
        # 256 LSTM neurons
        self.UNITS = 256
        # 40% dropout
        self.DROPOUT = 0.4
        # whether to use bidirectional RNNs
        self.BIDIRECTIONAL = False
        # training parameters
        # mean absolute error loss
        # LOSS = "mae"
        # huber loss
        self.LOSS = "huber_loss"
        self.OPTIMIZER = "adam"
        self.BATCH_SIZE = 64
        self.EPOCHS = 50
        # Amazon stock market
        self.ticker = "AMZN"

    args = {
        'ticker': fields.Str(
            required=True,
            default='AMZN'
        ),
        'steps': fields.Int(
            required=False,
            default=50
        ),
        'scale': fields.Bool(
            required=False,
            default=False
        ),
        'split_by_date': fields.Bool(
            required=False,
            default=False
        ),
        'cols': fields.Str(
            required=True
        ),
        'test_size': fields.Float(
            required=True,
            validate=validate.Range(0, 1)
        ),
        'shuffle': fields.Bool(
            required=False
        ),
        'look_step': fields.Int(
            required=False,
            validate=validate.Range(1, 30)
        ),
    }

    @use_kwargs(args, location="query")
    def get(
            self,
            ticker: str,
            steps: int,
            scale: bool,
            split_by_date: bool,
            cols: str,
            test_size: float,
            shuffle: bool,
            look_step: int):

        feature_cols = []
        if len(cols):
            feature_cols = cols.split(',')
        print(ticker, steps, scale, split_by_date, feature_cols)
        data = self.helper.load_stock_data(
            ticker=ticker,
            n_steps=steps,
            scale=scale,
            split_by_date=split_by_date,
            shuffle=shuffle,
            lookup_step=look_step,
            test_size=test_size,
            feature_columns=feature_cols
        )
        # print()
        # testdata = data["df"].to_csv()
        # print(testdata)
        # parsed = json.loads(jsonDt)
        # print(json.dumps(parsed, indent=4))
        # return json.dumps(parsed, indent=4)
        # return None, 200
        model = self.create_model(
            sequence_length=steps,
            n_features=len(feature_cols),
            units=self.UNITS,
            cell=self.CELL,
            n_layers=self.N_LAYERS,
            dropout=self.DROPOUT,
            loss=self.LOSS,
            optimizer=self.OPTIMIZER,
            bidirectional=self.BIDIRECTIONAL
        )
        history = model.fit(
            data["X_train"],
            data["y_train"],
            batch_size=self.BATCH_SIZE,
            epochs=self.EPOCHS,
            validation_data=(data["X_test"], data["y_test"]),
            verbose=1
        )
        # save to json:
        # self.save_files(hist_json_file, history)

        # Predict Model ,Data
        future_price = self.predict(model, data, scale=scale)

        # evaluate the model
        loss, mae = model.evaluate(data["X_test"], data["y_test"], verbose=0)
        # calculate the mean absolute error (inverse scaling)
        if scale:
            mean_absolute_error = data["column_scaler"]["adjclose"].inverse_transform([[mae]])[
                0][0]
        else:
            mean_absolute_error = mae

        # get the final dataframe for the testing set
        final_df = self.get_final_df(
            model, data, scale=scale, look_step=look_step)

        # we calculate the accuracy by counting the number of positive profits
        accuracy_score = (len(final_df[final_df['sell_profit'] > 0]) +
                          len(final_df[final_df['buy_profit'] > 0])) / len(final_df)
        # calculating total buy & sell profit
        total_buy_profit = final_df["buy_profit"].sum()
        total_sell_profit = final_df["sell_profit"].sum()
        # total profit by adding sell & buy together
        total_profit = total_buy_profit + total_sell_profit
        # dividing total profit by number of testing samples (number of trades)
        profit_per_trade = total_profit / len(final_df)

        print(
            f"Future price after {look_step} days is {future_price:.2f}$")

        return jsonify({
            'future_price': future_price,
            'accuracy_score': accuracy_score,
            'total_buy_profit': total_buy_profit,
            'total_sell_profit': total_sell_profit,
            'total_profit': total_profit,
            'profit_per_trade': profit_per_trade,
            # 'data': json.dumps({'data': data.tolist() })
        }), 200

    def save_files(self, file_name: str, history):
        hist_df = pd.DataFrame(history.history)
        with open(file_name, mode='w') as f:
            hist_df.to_json(f)
        pass

    def create_model(self, sequence_length, n_features, units=256, cell=LSTM, n_layers=2, dropout=0.3,
                     loss="mean_absolute_error", optimizer="rmsprop", bidirectional=False):
        model = tf.keras.models.Sequential()

        for i in range(n_layers):
            if i == 0:
                # first layer
                if bidirectional:
                    model.add(tf.keras.layers.Bidirectional(cell(units, return_sequences=True), batch_input_shape=(
                        None, sequence_length, n_features)))
                else:
                    model.add(cell(units, return_sequences=True, batch_input_shape=(
                        None, sequence_length, n_features)))
            elif i == n_layers - 1:
                # last layer
                if bidirectional:
                    model.add(tf.keras.layers.Bidirectional(
                        cell(units, return_sequences=False)))
                else:
                    model.add(cell(units, return_sequences=False))
            else:
                # hidden layers
                if bidirectional:
                    model.add(tf.keras.layers.Bidirectional(
                        cell(units, return_sequences=True)))
                else:
                    model.add(cell(units, return_sequences=True))
            # add dropout after each layer
            model.add(Dropout(dropout))
        model.add(Dense(1, activation="linear"))
        model.compile(loss=loss, metrics=[
                      "mean_absolute_error"], optimizer=optimizer)
        return model

    def predict(self, model, data, scale: bool):
        # retrieve the last sequence from data
        last_sequence = data["last_sequence"][-self.N_STEPS:]
        # expand dimension
        last_sequence = np.expand_dims(last_sequence, axis=0)
        # get the prediction (scaled from 0 to 1)
        prediction = model.predict(last_sequence)
        # get the price (by inverting the scaling)
        if scale:
            predicted_price = data["column_scaler"]["adjclose"].inverse_transform(prediction)[
                0][0]
        else:
            predicted_price = prediction[0][0]
        return predicted_price

    def get_final_df(self, model, data, scale: bool, look_step: int):
        """
        This function takes the `model` and `data` dict to
        construct a final dataframe that includes the features along
        with true and predicted prices of the testing dataset
        """
        # if predicted future price is higher than the current,
        # then calculate the true future price minus the current price, to get the buy profit
        def buy_profit(current, pred_future, true_future): return true_future - \
            current if pred_future > current else 0
        # if the predicted future price is lower than the current price,
        # then subtract the true future price from the current price
        def sell_profit(current, pred_future, true_future): return current - \
            true_future if pred_future < current else 0
        X_test = data["X_test"]
        y_test = data["y_test"]
        # perform prediction and get prices
        y_pred = model.predict(X_test)
        if scale:
            y_test = np.squeeze(data["column_scaler"]["adjclose"].inverse_transform(
                np.expand_dims(y_test, axis=0)))
            y_pred = np.squeeze(data["column_scaler"]
                                ["adjclose"].inverse_transform(y_pred))
        test_df = data["test_df"]
        # add predicted future prices to the dataframe
        test_df[f"adjclose_{look_step}"] = y_pred
        # add true future prices to the dataframe
        test_df[f"true_adjclose_{look_step}"] = y_test
        # sort the dataframe by date
        test_df.sort_index(inplace=True)
        final_df = test_df
        # add the buy profit column
        final_df["buy_profit"] = list(map(buy_profit,
                                          final_df["adjclose"],
                                          final_df[f"adjclose_{look_step}"],
                                          final_df[f"true_adjclose_{look_step}"])
                                      # since we don't have profit for last sequence, add 0's
                                      )
        # add the sell profit column
        final_df["sell_profit"] = list(map(sell_profit,
                                           final_df["adjclose"],
                                           final_df[f"adjclose_{look_step}"],
                                           final_df[f"true_adjclose_{look_step}"])
                                       # since we don't have profit for last sequence, add 0's
                                       )
        return final_df


class PredictionHistory(Resource):
    def get(self, id):
        df = pd.read_json('history.json')
        return df
