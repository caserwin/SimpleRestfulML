# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 下午2:45
# @Author  : yidxue

import os
import pickle
import numpy as np
from src.handler.base.base_handler import BaseHandler

module_path = os.path.abspath(os.path.join(os.curdir))
model_path = os.path.join(module_path, 'model')


class IrisPredictHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(IrisPredictHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        sepal_length = float(self.get_argument('sepal_length', 2.0))
        sepal_width = float(self.get_argument('sepal_width', 2.0))
        petal_length = float(self.get_argument('petal_length', 2.0))
        petal_width = float(self.get_argument('petal_width', 2.0))

        # 读取模型
        lr_model = pickle.load(open(os.path.join(model_path, 'lr_iris.model'), 'rb'))

        # 预测
        index = lr_model.predict(np.array([[sepal_length, sepal_width, petal_length, petal_width]]))[0]
        target = lr_model.get_target_name()[index]
        self.set_result(result={"label": target})
