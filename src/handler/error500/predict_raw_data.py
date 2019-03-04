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
        timestamp = self.get_argument('timestamp', "1")
        value = float(self.get_argument('value', 0.0))
        # 预测
        rc = RedisClient()
        res_ls = rc.get_cache_data("error500")
        res_dic = {json.loads(item)["ds"]: float(json.loads(item)["yhat_upper"]) for item in res_ls}
        print(res_dic)

        pred_value = res_dic.get(timestamp, -1)
        if value >= pred_value:
            self.set_result({"label": 1, "yhat_upper": pred_value})
        else:
            self.set_result({"label": 0, "yhat_upper": pred_value})
