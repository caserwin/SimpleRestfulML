# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 下午2:22
# @Author  : yidxue
import pickle
import json


class RenameUnpickler(pickle.Unpickler):
    """
    https://stackoverflow.com/questions/27732354/unable-to-load-files-using-pickle-and-multiple-modules
    """

    def find_class(self, module, name):
        if name == 'LogisticRegressionTrain':
            from src.train.lr_train import LogisticRegressionTrain
            return LogisticRegressionTrain
        if name == 'DecisionTreeTrain':
            from src.train.dt_train import DecisionTreeTrain
            return DecisionTreeTrain

        return super(RenameUnpickler, self).find_class(module, name)


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
    except UnicodeDecodeError:
        return pickle.load(fr)
    except ModuleNotFoundError:
        return RenameUnpickler(fr).load()
    except AttributeError:
        return RenameUnpickler(fr).load()


def check_json(input_str):
    try:
        json.loads(input_str)
        return True
    except:
        return False


def to_bool(input_str):
    return input_str.lower() in ("yes", "true", "1")
