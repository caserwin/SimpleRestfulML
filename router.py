#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.handler.description_handler import DescriptionHandler
from src.handler.compute_handler import SimpleComputeHandler
from src.handler.iris_predict_handler import IrisPredictHandler
from src.handler.error500.load_raw_data import LoadRawDataHandler
from src.handler.error500.train_raw_data import TrainRawDataHandler
from src.handler.error500.predict_raw_data import PredictRawDataHandler

url_map = [
    (r"/description", DescriptionHandler),
    (r"/compute", SimpleComputeHandler),
    (r"/iris_predict", IrisPredictHandler),
    (r"/error500/load_data", LoadRawDataHandler),
    (r"/error500/train_data", TrainRawDataHandler),
    (r"/error500/predict_data", PredictRawDataHandler)
]
