# -*- coding: utf-8 -*-
# @Time    : 2019/3/1 下午1:21
# @Author  : yidxue
import os
import time
import pandas as pd
from src.db.mysql_db import error500
from src.handler.base.base_handler import BaseHandler
from src.utils.script import create_table_sql
from src.utils import config

module_path = os.path.abspath(os.path.join(os.curdir))
data_path = os.path.join(module_path, 'data')


class LoadRawDataHandler(BaseHandler):

    def __init__(self, application, request, **kwargs):
        super(LoadRawDataHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        operDF = pd.read_json(os.path.join(data_path, 'mng20days_B.json'))
        raw_values = operDF.values.tolist()
        values = [(int(time.mktime(time.strptime(str(value[0]), '%Y-%m-%d %H:%M:%S'))), str(value[0]), value[1]) for
                  value in raw_values]

        # mysql 连接
        name = config.get("mysql_table_error500_raw_data", "name")
        cols = config.get("mysql_table_error500_raw_data", "col").split(', ')
        types = config.get("mysql_table_error500_raw_data", "type").split(', ')
        primarys = config.get("mysql_table_error500_raw_data", "primary").split(', ')
        comments = config.get("mysql_table_error500_raw_data", "comment").split(', ')

        error500().execute(create_table_sql(name, cols, types, primarys, comments))

        values = [{
            "timestamp": value[0],
            "date": value[1],
            "value": value[2],
        } for value in values]

        error500().insert_batch(name, values)
        self.set_result({"message": "succeed to insert ignore {num} rows to {name}".format(num=len(values), name=name)})
