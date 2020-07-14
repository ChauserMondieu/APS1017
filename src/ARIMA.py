from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error
import datetime
import pandas as pd
import os
import time
# ignore warning
import warnings
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")


class Arima(object):
    df = pd.DataFrame()
    client_models = dict()
    material_models = dict()
    client_material_models = dict()
    directory = os.path.join(os.getcwd(), "static")
    orders = 0

    @classmethod
    def store_df(cls, dir):
        file_name = 'APS1017 Order data for Project.csv'
        data = os.path.join(dir, file_name)
        # import data
        Arima.df = pd.read_csv(data)
        # Get rid of duplicate data
        Arima.df.drop_duplicates()

        # convert the date to pandas date type
        Arima.df['Date'] = pd.to_datetime(Arima.df['Date'])

        # sort the date on ascending order which is very important for the model training !
        Arima.df = Arima.df.sort_values(by=['Date'], ascending=True)

    # evaluate combinations of p, d and q values for an ARIMA model
    @classmethod
    def evaluate_models(cls, dataset, p_values, d_values, q_values):
        dataset = dataset.astype('float32')

        # get the best score for the model
        best_score, best_cfg = float("inf"), None
        for p in p_values:
            for d in d_values:
                for q in q_values:
                    order = (p, d, q)
                    # try different combination to find best one
                    try:
                        # evaluate an ARIMA model for a given order (p,d,q)
                        def evaluate_arima_model(X, arima_order):
                            # prepare training dataset
                            train_size = int(len(X) * 0.66)

                            # split the train and test set
                            train, test = X[0:train_size], X[train_size:]

                            history = [x for x in train]

                            # make predictions
                            predictions = list()

                            for t in range(len(test)):
                                model = ARIMA(history, order=arima_order)
                                model_fit = model.fit(disp=0)
                                yhat = model_fit.forecast()[0]
                                predictions.append(yhat)
                                history.append(test[t])

                            # calculate out of sample error
                            error = mean_squared_error(test, predictions)
                            return error

                        # try different combination to find best one
                        mse = evaluate_arima_model(dataset, order)
                        if mse < best_score:
                            best_score, best_cfg = mse, order
                        print('ARIMA%s MSE=%.3f' % (order, mse))
                    except:
                        continue
        return best_cfg, best_score

    # x is the given client
    @classmethod
    def only_client(cls, x, date):
        tmp_df = Arima.df[Arima.df.Client == str(x)][["Date", "Order Quantity"]]

        # get the history of date and the Order quantity on that date of given client : x
        check = tmp_df.groupby("Date").sum()

        # find out which day client x put an order, get the min and max date
        time_index = pd.date_range(min(check.index), max(check.index), freq='D')

        # store the date when client put an order
        check = check.reindex(time_index, fill_value=0)

        p_values = [1, 2, 3]
        d_values = range(0, 3)
        q_values = range(0, 3)

        t = cls.evaluate_models(check['Order Quantity'], p_values, d_values, q_values)

        history = [x for x in check['Order Quantity']]
        model = ARIMA(history, order=t[0])
        model_fit = model.fit(disp=0)

        # enddate : the date I want to predict
        enddate = datetime.datetime.strptime(date, '%Y-%m-%d')

        # max(check.index) is the last day client x put an order

        delta = enddate - max(check.index)

        # do the prediction
        forecast = model_fit.predict(start=len(check["Order Quantity"]),
                                     end=len(check["Order Quantity"]) + delta.days)

        Forecast = pd.DataFrame(forecast)
        Forecast.columns = ['Forecast']

        # update the date informations
        end_date = max(check.index) + datetime.timedelta(days=delta.days)
        time_index = pd.date_range(max(check.index), end_date, freq='D')
        Forecast = Forecast.set_index(time_index)

        plt.figure(figsize=(20, 10))
        plt.plot(check.index, check['Order Quantity'], label='History')
        plt.plot(Forecast.index, Forecast['Forecast'], label='Forecast')
        plt.legend(loc='best')
        file_name = str(x) + ".png"
        file_path = os.path.join(Arima.directory, file_name)
        plt.savefig(file_path, dpi=400, facecolor='w', edgecolor='w',
                    bbox_inches='tight')
        plt.close()
        return Forecast.at[date, "Forecast"], file_name

    # evaluate parameters
    # when only material is given
    @classmethod
    def only_material(cls, y, date):
        tmp_df = Arima.df[Arima.df.Material == int(y)][["Date", "Order Quantity"]]
        check = tmp_df.groupby("Date").sum()
        time_index = pd.date_range(min(check.index), max(check.index), freq='D')
        check = check.reindex(time_index, fill_value=0)
        p_values = [1, 2, 3]
        d_values = range(0, 3)
        q_values = range(0, 3)
        t = cls.evaluate_models(check['Order Quantity'], p_values, d_values, q_values)
        history = [x for x in check['Order Quantity']]
        model = ARIMA(history, order=t[0])
        model_fit = model.fit(disp=0)

        enddate = datetime.datetime.strptime(date, '%Y-%m-%d')

        delta = enddate - max(check.index)
        forecast = model_fit.predict(start=len(check["Order Quantity"]),
                                     end=len(check["Order Quantity"]) + delta.days)

        Forecast = pd.DataFrame(forecast)

        Forecast.columns = ['Forecast']
        end_date = max(check.index) + datetime.timedelta(days=delta.days)
        time_index = pd.date_range(max(check.index), end_date, freq='D')
        Forecast = Forecast.set_index(time_index)

        plt.figure(figsize=(20, 10))
        plt.plot(check.index, check['Order Quantity'], label='History')
        plt.plot(Forecast.index, Forecast['Forecast'], label='Forecast')
        plt.legend(loc='best')
        file_name = str(y) + ".png"
        file_path = os.path.join(Arima.directory, file_name)
        plt.savefig(file_path, dpi=400, facecolor='w', edgecolor='w',
                    bbox_inches='tight')
        plt.close()
        return Forecast.at[date, "Forecast"], file_name

    @classmethod
    def both_material_client(cls, x, y, date):
        tmp_df = Arima.df[(Arima.df.Material == int(y)) & (Arima.df.Client == str(x))][["Date", "Order Quantity"]]
        check = tmp_df.groupby("Date").sum()
        time_index = pd.date_range(min(check.index), max(check.index), freq='D')
        check = check.reindex(time_index, fill_value=0)
        p_values = [1, 2, 3]
        d_values = range(0, 3)
        q_values = range(0, 3)
        t = cls.evaluate_models(check['Order Quantity'], p_values, d_values, q_values)
        history = [x for x in check['Order Quantity']]
        model = ARIMA(history, order=t[0])
        model_fit = model.fit(disp=0)
        enddate = datetime.datetime.strptime(date, '%Y-%m-%d')

        delta = enddate - max(check.index)
        forecast = model_fit.predict(start=len(check["Order Quantity"]),
                                     end=len(check["Order Quantity"]) + delta.days)

        Forecast = pd.DataFrame(forecast)

        Forecast.columns = ['Forecast']
        end_date = max(check.index) + datetime.timedelta(days=delta.days)
        time_index = pd.date_range(max(check.index), end_date, freq='D')
        Forecast = Forecast.set_index(time_index)
        plt.figure(figsize=(20, 10))
        plt.plot(check.index, check['Order Quantity'], label='History')
        plt.plot(Forecast.index, Forecast['Forecast'], label='Forecast')
        plt.legend(loc='best')
        file_name = str(x) + str(y) + ".png"
        file_path = os.path.join(Arima.directory, file_name)
        plt.savefig(file_path, dpi=400, facecolor='w', edgecolor='w',
                    bbox_inches='tight')
        plt.close()
        return Forecast.at[date, "Forecast"], file_name

    @classmethod
    def ARIMA_main(cls, directory, client, material, date):
        dates = time.strftime("%Y-%m-%d", time.strptime(date, "%Y/%m/%d"))
        cls.store_df(directory)
        if client == "all":
            return cls.only_material(material, dates)
        elif material == "all":
            return cls.only_client(client, dates)
        else:
            return cls.both_material_client(client, material, dates)


'''
if __name__ == "__main__":
    print(Arima.ARIMA_main(os.path.join(os.path.dirname(os.getcwd()), "dat"), client='c5', material=12246740, date='2020/03/01'))
'''
