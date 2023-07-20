import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt


class PredictService:
    def __init__(self):
        pass

    def create_model(self, sequence_length, n_features, units=256, cell=tf.keras.layers.LSTM, n_layers=2, dropout=0.3,
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
            model.add(tf.keras.layers.Dropout(dropout))
        model.add(tf.keras.layers.Dense(1, activation="linear"))
        model.compile(loss=loss, metrics=[
                      "mean_absolute_error"], optimizer=optimizer)
        return model

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

    def predict(self, model, data, scale: bool, n_steps: int):
        # retrieve the last sequence from data
        last_sequence = data["last_sequence"][-n_steps:]
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

    def save_history(self, file_name: str, history) -> None:
        hist_df = pd.DataFrame(history.history)
        with open(file_name, mode='w') as f:
            hist_df.to_json(f)

    def plot_graph(self, test_df, lookup_step):
        """
        This function plots true close price along with predicted close price
        with blue and red colors respectively
        """
        plt.plot(test_df[f'true_adjclose_{lookup_step}'], c='b')
        plt.plot(test_df[f'adjclose_{lookup_step}'], c='r')
        plt.xlabel("Days")
        plt.ylabel("Price")
        plt.legend(["Actual Price", "Predicted Price"])
        plt.show()
