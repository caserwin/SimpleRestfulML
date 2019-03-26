#!/usr/bin/python
# -*- coding: utf-8 -*-

from src.handler.test.compute_handler import SimpleComputeHandler
from src.handler.test.multi_process_test import MultiProcessHandler

from src.handler.description_handler import DescriptionHandler
from src.handler.reload_model_handler import ReloadModelHandler
from src.handler.upload_model_handler import FileUploadHandler

from src.handler.dbtest.predict_raw_data_handler import PredictRawDataHandler
from src.handler.dbtest.train_raw_data_handler import TrainRawDataHandler
from src.handler.iris.lr_predict_handler import LRPredictHandler
from src.handler.iris.dt_predict_handler import DTPredictHandler

url_map = [
    (r"/test/description", DescriptionHandler),
    (r"/test/multiprocess", MultiProcessHandler),

    (r"/compute", SimpleComputeHandler),
    (r"/iris/lr_predict", LRPredictHandler),
    (r"/iris/dt_predict", DTPredictHandler),
    (r"/dbtest/train_data", TrainRawDataHandler),
    (r"/dbtest/predict_data", PredictRawDataHandler),
    (r"/reload_model", ReloadModelHandler),
    (r"/upload_model", FileUploadHandler)
]
