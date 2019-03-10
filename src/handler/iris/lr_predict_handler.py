# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 下午2:45
# @Author  : yidxue
import numpy as np
from tornado.options import options
from src.handler.base.base_handler import BaseHandler
from src.utils.error import Error

USE_MODEL_NAME = 'lr_iris.model'


class LRPredictHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(LRPredictHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        # 获取参数
        sepal_length = float(self.get_argument('sepal_length', 2.0))
        sepal_width = float(self.get_argument('sepal_width', 2.0))
        petal_length = float(self.get_argument('petal_length', 2.0))
        petal_width = float(self.get_argument('petal_width', 2.0))
        self.set_result(result={"label": 11})

        # 预测
        model = options.models.get(USE_MODEL_NAME, None)
        if model is None:
            self.set_error(error_code=Error.ERROR_CODE1,
                           error_message="{model} is None, please reload models!".format(model=USE_MODEL_NAME))
            return

        index = model.predict(np.array([[sepal_length, sepal_width, petal_length, petal_width]]))[0]
        target = model.get_target_name()[index]
        self.set_result(result={"label": target, "model": USE_MODEL_NAME, "version": model.version})
