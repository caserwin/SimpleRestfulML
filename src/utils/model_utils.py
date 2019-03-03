# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 下午2:22
# @Author  : yidxue
import pickle


def store_model(model, filename):
    fw = open(filename, 'wb')
    # 对象持久化包
    pickle.dump(model, fw)
    fw.close()


def read_model(filename):
    fr = open(filename, 'rb')
    print("load model {filename}".format(filename = filename))
    return pickle.load(fr)
