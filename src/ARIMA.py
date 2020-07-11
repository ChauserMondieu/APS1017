import pmdarima as pm
from statsmodels.tsa.arima_model import ARIMA
import pandas as pd
import os


class ARIMA(object):
    df = pd.DataFrame()
    client_models = dict()
    material_models = dict()
    client_material_models = dict()
    orders = 0

    @classmethod
    def store_df(cls, dir):
        file_name = 'APS1017 Order data for Project.csv'
        data = os.path.join(dir, file_name)
        # import data
        ARIMA.df = pd.read_csv(data)
        # Get rid of duplicate data
        ARIMA.df.drop_duplicates()

        # convert the date to pandas date type
        ARIMA.df['Date'] = pd.to_datetime(ARIMA.df['Date'])

        # sort the date on ascending order which is very important for the model training !
        ARIMA.df = ARIMA.df.sort_values(by=['Date'], ascending=True)

    @classmethod
    def ARIMA_training(cls):
        for c in ARIMA.df.Client.unique():
            df_tmp = ARIMA.df[ARIMA.df.Client == c][
                ['Date', 'Order Quantity']]  # df_tmp :  classify date and quantity based on client

            last_date = df_tmp['Date'].tolist()[-1]
            df_tmp = df_tmp.set_index('Date')  # use Date as index

            ts = df_tmp['Order Quantity']  # ts : target
            m = pm.ARIMA(order=(2, 2, 2))  # m is the model ， （2，2，2） are the parameter I choosed
            z = m.fit(ts)
            ARIMA.client_models[c] = [last_date, z]

        for mm in ARIMA.df.Material.unique():
            df_tmp = ARIMA.df[ARIMA.df.Material == mm][['Date', 'Order Quantity']]
            last_date = df_tmp['Date'].tolist()[-1]
            df_tmp = df_tmp.set_index('Date')
            #   print(df_tmp.head())
            ts = df_tmp['Order Quantity']
            m = pm.ARIMA(order=(2, 2, 2))
            z = m.fit(ts)
            ARIMA.material_models[mm] = [last_date, z]

        for mm in ARIMA.df.Material.unique():
            df_tmp = ARIMA.df[ARIMA.df.Material == mm]
            cc = df_tmp.Client.unique()
            for c in cc:
                df_c_tmp = df_tmp[df_tmp.Client == c][['Date', 'Order Quantity']]
                last_date = df_c_tmp['Date'].tolist()[-1]
                df_c_tmp = df_c_tmp.set_index('Date')
                ts = df_c_tmp['Order Quantity']
                m = pm.ARIMA(order=(2, 2, 2))
                try:
                    z = m.fit(ts)
                    ARIMA.client_material_models[str(mm) + '_c_' + c] = [last_date, z]
                except:
                    continue

    @classmethod
    def ARIMA_Prediction(cls, client, material, d):
        # Material model
        if client == "all":
            try:
                element = ARIMA.material_models[material]
                last_date = element[0]
                length = (d - last_date).days
                result = element[1].predict(length, return_conf_int=True, alpha=0.05)[0][length - 1]
                ARIMA.orders = round(result)
                return ARIMA.orders
            except:
                return ARIMA.orders
        # client model
        elif material == "all":
            try:
                element = ARIMA.client_models[client]
                last_date = element[0]
                length = (d - last_date).days
                result = element[1].predict(length, return_conf_int=True, alpha=0.05)[0][length - 1]
                ARIMA.orders = round(result)
                return ARIMA.orders
            except:
                return ARIMA.orders

        # both are given
        else:
            try:
                element = ARIMA.client_material_models[str(material) + '_c_' + client]
                last_date = element[0]
                length = (d - last_date).days
                result = element[1].predict(length, return_conf_int=True, alpha=0.05)[0][length - 1]
                ARIMA.orders = round(result)
                return ARIMA.orders
            except:
                return ARIMA.orders

    @classmethod
    def ARIMA(cls, directory, client, material, date):
        dates = pd.to_datetime(date, format="%Y/%m/%d")
        ARIMA.store_df(directory)
        ARIMA.ARIMA_training()
        return ARIMA.ARIMA_Prediction(client, material, dates)
