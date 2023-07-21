from flask_restful import Resource
from flask import abort
import numpy as np
import json
import random
import tensorflow as tf
import time
from resources.helpers import Helpers
from webargs import fields
from webargs.flaskparser import use_kwargs
from resources.services.predict import PredictService
from resources.services.filters import FilterService
from resources.models.filters import Filters
from resources.models.predictions_history import PredictionsHistory, PredictionsHistoryQuery


class Predict(Resource):
    def __init__(self):
        self.helper = Helpers()
        self.service = PredictService()
        self.filter_service = FilterService()
        self.history_service = PredictionsHistoryQuery()
        # set seed, so we can get the same results after rerunning several times
        np.random.seed(314)
        tf.random.set_seed(314)
        random.seed(314)
        # whether to split the training/testing set by date
        self.SPLIT_BY_DATE = False
        self.split_by_date_str = f"sbd-{int(self.SPLIT_BY_DATE)}"
        # features to use
        # date now
        self.date_now = time.strftime("%Y-%m-%d")
        # model parameters
        self.N_LAYERS = 2
        # LSTM cell
        self.CELL = tf.keras.layers.LSTM
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
    get_args = {
        'id': fields.Str(
            required=True
        )
    }
    post_args = {
        'filter_id': fields.Str(
            required=True
        )
    }

    @use_kwargs(get_args, location='query')
    def get(self, id: str):
        data = self.history_service.findOneById(id)
        return data.serialize, 200

    @use_kwargs(post_args)
    def post(self, filter_id: str):
        # Check exits filter on prediction history
        if (self.history_service.checkExistFilter(filter_id=filter_id) == True):
            abort(400, f'Filter Exits , {filter_id}')
        # Find Filter Id
        requestFilter: Filters = self.filter_service.getFilterById(filter_id)
        feature_cols = []
        if len(requestFilter.cols):
            feature_cols = requestFilter.cols.split(',')

        # Loads data
        data = self.helper.load_stock_data(
            ticker=requestFilter.serialize['ticker'],
            n_steps=requestFilter.steps,
            scale=requestFilter.scale,
            split_by_date=requestFilter.split_by_date,
            shuffle=requestFilter.shuffle,
            lookup_step=requestFilter.look_step,
            test_size=requestFilter.test_size,
            feature_columns=feature_cols
        )

        # Create Model
        model = self.service.create_model(
            sequence_length=requestFilter.steps,
            n_features=len(feature_cols),
            units=requestFilter.units,
            cell=self.CELL,
            n_layers=self.N_LAYERS,
            dropout=self.DROPOUT,
            loss=self.LOSS,
            optimizer=self.OPTIMIZER,
            bidirectional=self.BIDIRECTIONAL
        )

        # fit history
        history = model.fit(
            data["X_train"],
            data["y_train"],
            batch_size=requestFilter.batch_size,
            epochs=requestFilter.epochs,
            validation_data=(data["X_test"], data["y_test"]),
            verbose=1
        )

        # Predict Model ,Data
        future_price = self.service.predict(
            model, data, scale=requestFilter.scale, n_steps=requestFilter.n_steps)

        # evaluate the model
        loss, mae = model.evaluate(data["X_test"], data["y_test"], verbose=0)
        # calculate the mean absolute error (inverse scaling)
        if requestFilter.scale:
            mean_absolute_error = data["column_scaler"]["adjclose"].inverse_transform([[mae]])[
                0][0]
        else:
            mean_absolute_error = mae

        # get the final dataframe for the testing set
        final_df = self.service.get_final_df(
            model, data, scale=requestFilter.scale, look_step=requestFilter.look_step)

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

        response = {
            'loss': str(loss),
            'future_price': str(future_price),
            'accuracy_score': str(accuracy_score),
            'total_buy_profit': str(total_buy_profit),
            'total_sell_profit': str(total_sell_profit),
            'total_profit': str(total_profit),
            'profit_per_trade': str(profit_per_trade),
            'mean_absolute_error': str(mean_absolute_error)
        }
        # store
        model = PredictionsHistory()
        model.loss = str(loss)
        model.accuracy_score = str(accuracy_score)
        model.profit_per_trade = str(profit_per_trade)
        model.future_price = str(future_price)
        model.total_buy_profit = str(total_buy_profit)
        model.total_sell_profit = str(total_sell_profit)
        model.total_profit = str(total_profit)
        model.user_id = str(requestFilter.user_id)
        model.filter_id = str(requestFilter.id)

        try:
            self.history_service.save(model)
        except:
            abort(500, 'Save model error')

        return response, 201


class StockData(Resource):
    def __init__(self) -> None:
        self.helper = Helpers()

    args = {
        'ticker': fields.Str(
            required=True
        )
    }

    @use_kwargs(args, location='query')
    def get(self, ticker: str):
        data = self.helper.load_df_ticker(ticker=ticker)
        # print(data)
        return data, 200
