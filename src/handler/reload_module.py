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
        print("hhhhhhhhh")
        # filename = self.get_argument('filename', 'lr_iris.model')
        # lr_model = read_model(os.path.join(model_path, filename))
        # self.update_model(filename, lr_model)
