# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 下午2:22
# @Author  : yidxue
import pickle
import json


def store_model(model, filename):
    fw = open(filename, 'wb')
    # 对象持久化包
    pickle.dump(model, fw)
    fw.close()


def read_model(filename):
    fr = open(filename, 'rb')
    print("load model {filename}".format(filename=filename))
    try:
        return pickle.load(fr, encoding='latin1')
    except:
        return pickle.load(fr)


def check_json(input_str):
    try:
        json.loads(input_str)
        return True
    except:
        return False


def to_bool(input_str):
    return input_str.lower() in ("yes", "true", "1")