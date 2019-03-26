#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-03-26 09:51
# @Author  : erwin
from src.handler.base.base_handler import BaseHandler
import time


class MultiProcessHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(MultiProcessHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        time.sleep(10)
        self.set_result({"message": "sleep 10 seconds !!"})
