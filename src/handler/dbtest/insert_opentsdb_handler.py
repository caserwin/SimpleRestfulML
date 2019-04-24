#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-12 15:48
# @Author  : erwin
from src.db.opentsdb_conn import OpenTSDBClient
from src.handler.base.base_handler import BaseHandler
import time


class OpenTSDBRawDataHandler(BaseHandler):

    def __init__(self, application, request, **kwargs):
        super(OpenTSDBRawDataHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        # data source
        raw_values = [
            {'date': '2019-01-01 00:01:00', 'col1': 1.1, 'col2': 2.1},
            {'date': '2019-02-01 00:02:00', 'col1': 1.2, 'col2': 2.2},
            {'date': '2019-03-01 00:03:00', 'col1': 1.3, 'col2': 2.3},
            {'date': '2019-04-01 00:04:00', 'col1': 1.4, 'col2': 2.4},
            {'date': '2019-04-10 00:05:00', 'col1': 1.5, 'col2': 2.5}]

        # 插入opentsdb
        oc = OpenTSDBClient()
        tsdb_data = [{
            "metric": "sys.test",
            "timestamp": int(time.mktime(time.strptime(str(value.get("date", 0)), '%Y-%m-%d %H:%M:%S'))),
            "value": value.get("col1", 1.0),
            "tags": {
                "cluster": "B"
            }
        } for value in raw_values]

        # 2条一批次插入
        text = oc.bulk_insert(tsdb_data, 2)
        self.set_result({"message": text})
