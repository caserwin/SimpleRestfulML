# -*- coding: utf-8 -*-
# @Time    : 2019/3/5 下午3:05
# @Author  : yidxue
import os
import numpy as np
from src.handler.base.base_handler import BaseHandler
from src.utils.model_utils import read_model
from tornado.options import options

USE_MODEL_NAME = 'dt_iris.model'
# module_path = os.path.abspath(os.path.join(os.curdir))
# model_path = os.path.join(module_path, 'model')
# lr_model = read_model(os.path.join(model_path, USE_MODEL_NAME))


class DTPredictHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(DTPredictHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        # 获取参数
        sepal_length = float(self.get_argument('sepal_length', 2.0))
        sepal_width = float(self.get_argument('sepal_width', 2.0))
        petal_length = float(self.get_argument('petal_length', 2.0))
        petal_width = float(self.get_argument('petal_width', 2.0))

        # 预测
        # if self.get_model(USE_MODEL_NAME) is None:
        #     self.update_model(USE_MODEL_NAME, lr_model)

        model = options.models.get(USE_MODEL_NAME, None)

        index = model.predict(np.array([[sepal_length, sepal_width, petal_length, petal_width]]))[0]
        target = model.get_target_name()[index]
        self.set_result(result={"label": target, "model": USE_MODEL_NAME})
