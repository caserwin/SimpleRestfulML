# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 下午1:53
# @Author  : yidxue
import os
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from src.utils.tools import store_model

module_path = os.path.abspath(os.path.join(os.pardir, os.pardir))
model_path = os.path.join(module_path, 'model')


class LogisticRegressionTrain(object):

    def __init__(self, train_data=datasets.load_iris()):
        # set data
        self.train_data = train_data
        self.X = self.train_data.data
        self.Y = self.train_data.target
        # self model
        self.model = None
        self.version = 1.0

    def get_feature(self):
        return self.X

    def get_label(self):
        return self.Y

    def get_target_name(self):
        return self.train_data.target_names

    def get_feature_name(self):
        return self.train_data.target_names

    def train(self):
        self.model = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')
        self.model.fit(self.X, self.Y)

    def predict(self, npArray):
        return self.model.predict(npArray)


if __name__ == '__main__':
    # 训练
    lr_model = LogisticRegressionTrain()
    lr_model.train()
    # 存模型
    store_model(lr_model, os.path.join(model_path, 'lr_iris.model'))
