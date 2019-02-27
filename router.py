#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.handler.index_handler import IndexHandler
from src.handler.demo_handler import DemoHandler

url_map = [
    (r"/index", IndexHandler),
    (r"/demo", DemoHandler),
]
