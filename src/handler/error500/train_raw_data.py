# -*- coding: utf-8 -*-
# @Time    : 2019/3/1 下午2:25
# @Author  : yidxue
from src.handler.base.base_handler import BaseHandler
from src.db.redis_db import RedisClient
from src.db.mysql_db import error500
from src.service.error500_service import Error500CalService
from src.utils.script import create_table_sql
from src.utils import config
import time


class TrainRawDataHandler(BaseHandler):

    def __init__(self, application, request, **kwargs):
        super(TrainRawDataHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        # read from conf
        name = config.get("mysql_table_error500_raw_data", "name")
        cols = config.get("mysql_table_error500_raw_data", "col")
        fcst = Error500CalService.calculate(cols, name)

        # 删redis
        rc = RedisClient()
        rc.delete_key("error500")

        # 存redis
        pred_values = fcst.tail(288)[["ds", "yhat_upper"]].values.tolist()

        values = [{
            "key": "error500_" + str(value[0]),
            "ds": str(value[0]),
            "yhat_upper": str(value[1])
        } for value in pred_values]
        rc.set_cache_data(values)

        # mysql 建表
        name = config.get("mysql_table_error500_predict_data", "name")
        cols = config.get("mysql_table_error500_predict_data", "col").split(', ')
        types = config.get("mysql_table_error500_predict_data", "type").split(', ')
        primarys = config.get("mysql_table_error500_predict_data", "primary").split(', ')
        error500().execute(create_table_sql(name, cols, types, primarys))

        # 插入mysql
        raw_values = fcst.values.tolist()
        values = [{
            "timestamp": int(time.mktime(time.strptime(str(value[0]), '%Y-%m-%d %H:%M:%S'))),
            "date": str(value[0]),
            "trend": value[1],
            "trend_lower": value[2],
            "trend_upper": value[3],
            "yhat_lower": value[4],
            "yhat_upper": value[5],
            "additive_terms": value[6],
            "additive_terms_lower": value[7],
            "additive_terms_upper": value[8],
            "daily": value[9],
            "daily_lower": value[10],
            "daily_upper": value[11],
            "multiplicative_terms": value[12],
            "multiplicative_terms_lower": value[13],
            "multiplicative_terms_upper": value[14],
            "weekly": value[15],
            "weekly_lower": value[16],
            "weekly_upper": value[17],
            "yhat": value[18]
        } for value in raw_values]

        error500().insert_batch(name, values)
        self.set_result({"message": "succeed to insert ignore {num} rows to {name}".format(num=len(values), name=name)})
