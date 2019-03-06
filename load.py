# -*- coding: utf-8 -*-
# @Time    : 2019/3/6 上午10:16
# @Author  : yidxue

from tornado.options import options
from src.utils.model_utils import read_model
import os

module_path = os.path.abspath(os.path.join(os.curdir))
model_path = os.path.join(module_path, 'model')


def load_models():
    options.models['dt_iris.model'] = read_model(os.path.join(model_path, "dt_iris.model"))
    options.models['lr_iris.model'] = read_model(os.path.join(model_path, "lr_iris.model"))
