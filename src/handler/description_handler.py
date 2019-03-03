#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.handler.base.base_handler import BaseHandler


class DescriptionHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(DescriptionHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        # 调用set_result方法响应http请求
        self.set_result({"message": "this is restful API for machine learning. welcome !"})
