#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.handler.base.base_handler import BaseHandler


class IndexHandler(BaseHandler):

    def do_action(self):
        # 调用set_result方法响应http请求
        self.set_result({"result": "this is restful welcome"})
