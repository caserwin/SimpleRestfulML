# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 上午9:50
# @Author  : yidxue


class ComputeService(object):

    def __init__(self):
        pass

    @staticmethod
    def plus(a, b):
        """
        :param a:
        :param b:
        :return:
        """
        return a + b

    @staticmethod
    def divide(a, b):
        """
        :param a:
        :param b:
        :return:
        """
        return a / float(b)

    @staticmethod
    def multiply(a, b):
        """
        :param a:
        :param b:
        :return:
        """
        return a * b

    @staticmethod
    def minus(a, b):
        """
        :param a:
        :param b:
        :return:
        """
        return a - b
