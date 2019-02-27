#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.handler.description_handler import DescriptionHandler
from src.handler.compute_handler import SimpleComputeHandler
from src.handler.iris_predict_handler import IrisPredictHandler

url_map = [
    (r"/description", DescriptionHandler),
    (r"/compute", SimpleComputeHandler),
    (r"/iris_predict", IrisPredictHandler)
]
