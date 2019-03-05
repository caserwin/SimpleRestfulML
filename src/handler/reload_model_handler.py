# -*- coding: utf-8 -*-
# @Time    : 2019/3/5 上午9:55
# @Author  : yidxue
import os
from src.handler.base.base_handler import BaseHandler
from src.utils.model_utils import read_model

module_path = os.path.abspath(os.path.join(os.curdir))
model_path = os.path.join(module_path, 'model')


class ReloadModelHandler(BaseHandler):

    def __init__(self, application, request, **kwargs):
        super(ReloadModelHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        model_name = self.get_argument('modelname', None)
        if model_name is None:
            for model_name in os.listdir(model_path):
                model = read_model(os.path.join(model_path, model_name))
                self.update_model(model_name, model)
            self.set_result(result={"message": "server has reload all models"})
        else:
            model = read_model(os.path.join(model_path, model_name))
            self.update_model(model_name, model)
            self.set_result(result={"message": "server has reload {model}".format(model=model_name)})
