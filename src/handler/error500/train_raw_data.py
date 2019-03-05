# -*- coding: utf-8 -*-
# @Time    : 2019/3/1 下午2:25
# @Author  : yidxue
import time
from src.db.mysql_db import error500
from src.db.redis_db import RedisClient
from src.handler.base.base_handler import BaseHandler
from src.utils import config
from src.utils.script import create_table_sql


class TrainRawDataHandler(BaseHandler):

    def __init__(self, application, request, **kwargs):
        super(TrainRawDataHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        # 数据源
        raw_values = [
            {'date': '2018-10-10 00:01:00', 'col1': 1.1, 'col2': 2.1},
            {'date': '2018-10-10 00:02:00', 'col1': 1.2, 'col2': 2.2},
            {'date': '2018-10-10 00:03:00', 'col1': 1.3, 'col2': 2.3},
            {'date': '2018-10-10 00:04:00', 'col1': 1.4, 'col2': 2.4},
            {'date': '2018-10-10 00:05:00', 'col1': 1.5, 'col2': 2.5}]

        # 删redis
        rc = RedisClient()
        rc.delete_key("error500")

        # 存redis
        values = [{
            "key": "error500_" + str(value.get("date", "0")),
            "timestamp": str(value.get("date", "0")),
            "col1": str(value.get("col1", 1.0)),
            "col2": str(value.get("col2", 2.0)),
        } for value in raw_values]
        rc.set_cache_data(values)

        # mysql 建表
        name = config.get("mysql_error500_test", "name")
        cols = config.get("mysql_error500_test", "col").split(', ')
        types = config.get("mysql_error500_test", "type").split(', ')
        primarys = config.get("mysql_error500_test", "primary").split(', ')
        error500().execute(create_table_sql(name, cols, types, primarys))

        # 插入mysql
        values = [{
            "timestamp": int(time.mktime(time.strptime(str(value.get("date", 0)), '%Y-%m-%d %H:%M:%S'))),
            "date": value.get("date", "0"),
            "col1": value.get("col1", 1.0),
            "col2": value.get("col2", 1.0),
        } for value in raw_values]

        error500().insert_batch(name, values)
        self.set_result({"message": "succeed to insert ignore {num} rows to {name}".format(num=len(values), name=name)})
