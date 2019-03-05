#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.handler.compute_handler import SimpleComputeHandler
from src.handler.description_handler import DescriptionHandler
from src.handler.error500.predict_raw_data import PredictRawDataHandler
from src.handler.error500.train_raw_data import TrainRawDataHandler
from src.handler.iris.lr_predict_handler import LRPredictHandler
from src.handler.iris.dt_predict_handler import DTPredictHandler
from src.handler.reload_module import ReloadModelHandler

url_map = [
    (r"/description", DescriptionHandler),
    (r"/compute", SimpleComputeHandler),
    (r"/iris/lr_predict", LRPredictHandler),
    (r"/iris/dt_predict", DTPredictHandler),
    (r"/error500/train_data", TrainRawDataHandler),
    (r"/error500/predict_data", PredictRawDataHandler),
    (r"/reload_model", ReloadModelHandler)
]
