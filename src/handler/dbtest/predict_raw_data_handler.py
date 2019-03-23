# -*- coding: utf-8 -*-
# @Time    : 2019/3/2 下午10:00
# @Author  : yidxue
from src.db.redis_db import RedisClient
from src.handler.base.base_handler import BaseHandler
import json


class PredictRawDataHandler(BaseHandler):

    def __init__(self, application, request, **kwargs):
        super(PredictRawDataHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        timestamp = self.get_argument('timestamp', '2018-10-10 00:01:00')
        value = float(self.get_argument('value', '0.5'))
        # predict
        rc = RedisClient()
        res_ls = rc.get_cache_data("error500")
        res_dic = {json.loads(item)["timestamp"]: float(json.loads(item)["col1"]) for item in res_ls}
        print(res_dic)

        pred_value = res_dic.get(timestamp, -1)
        if value >= pred_value:
            self.set_result({"message": {"label": 1, "reference": pred_value, "true value": value}})
        else:
            self.set_result({"message": {"label": 0, "reference": pred_value, "true value": value}})
