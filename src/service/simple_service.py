# -*- coding: utf-8 -*-
# @Time    : 2019/2/27 上午9:50
# @Author  : yidxue


class SimpleService(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def tranform(self):
        result = ()
        if self.a > self.b:
            result = (0, self.a + self.b)
        elif self.a == self.b:
            result = (1, self.a + self.b)
        elif self.a < self.b:
            result = (2, self.a + self.b)

        return result
