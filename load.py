# -*- coding: utf-8 -*-
# @Time    : 2019/3/6 上午10:16
# @Author  : yidxue
from tornado.options import options
from src.utils.tools import read_model
import os

module_path = os.path.abspath(os.path.join(os.curdir))
model_path = os.path.join(module_path, 'model')


def load_models():
    for model_name in os.listdir(model_path):
        options.models[model_name] = read_model(os.path.join(model_path, model_name))
