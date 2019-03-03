# -*- coding: utf-8 -*-
# @Time    : 2019/3/4 上午12:19
# @Author  : yidxue
from fbprophet import Prophet
import numpy as np
import datetime
import time
import pandas as pd
from src.db.mysql_db import error500


class Error500CalService(object):
    def __init__(self):
        pass

    @staticmethod
    def calculate(cols, name):
        """
        :rtype:
        """
        # take pass n day raw data as train set
        before_day = 1000
        now_date = datetime.datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
        pass_date = (datetime.datetime.now() + datetime.timedelta(days=-before_day)).strftime("%Y-%m-%d") + " 00:00:00"

        now_timestamp = int(time.mktime(time.strptime(now_date, '%Y-%m-%d %H:%M:%S')))
        pass_timestamp = int(time.mktime(time.strptime(pass_date, '%Y-%m-%d %H:%M:%S')))

        sql = 'select {cols} from {name} where `timestamp` < {now_timestamp} and `timestamp` > {pass_timestamp}' \
            .format(cols=cols, name=name, now_timestamp=now_timestamp, pass_timestamp=pass_timestamp)

        # read raw data from mysql
        raw_data = error500().query(sql)
        operDF = pd.DataFrame.from_records(
            [{'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(raw['timestamp'])), 'value': raw['value']}
             for raw in raw_data])

        operDF.columns = ["timeMins", "500rate"]
        operDF = operDF.sort_values("timeMins").copy()
        tempS = pd.Series(data=np.array(operDF["500rate"]),
                          index=operDF["timeMins"].map(lambda x: pd.to_datetime(x).replace(second=0)))

        df = tempS.resample('5min').asfreq().iloc[0:5780]
        df.sort_index()

        finalDF = pd.DataFrame(df.sort_index().values, index=df.sort_index().index).dropna().reset_index()
        finalDF.columns = ['ds', 'y']

        m = Prophet(changepoint_prior_scale=0.001)
        m.fit(finalDF)

        future = m.make_future_dataframe(periods=120, freq='H')
        fcst = m.predict(future)

        return fcst
