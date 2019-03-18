#!/usr/bin/python
# -*- coding: utf-8 -*-a
import json
from src.utils import config
from src.db.torndb_long_conn import Connection


class MySQLHelper(object):
    _instance = None

    def __init__(self, host, user, password, database, charset='utf8'):

        if self._instance:
            return

        self.__class__._instance = Connection(
            host,
            database,
            user=user,
            password=password,
            connect_timeout=2,
            charset=charset
        )

    @classmethod
    def query(cls, sql, *parameters):
        # type: (object, object) -> object
        return cls._instance.query(sql, *parameters)

    @classmethod
    def query_one(cls, sql, *parameters):
        res = cls._instance.get(sql, *parameters)
        return res if res else {}

    @classmethod
    def delete(cls, sql, *parameters):
        return cls._instance.update(sql, *parameters)

    @classmethod
    def execute(cls, sql, *parameters):
        return cls._instance.execute(sql, *parameters)

    @classmethod
    def insert_dict(cls, tablename, rowdict, replace=False):
        return cls._instance.insert_dict(tablename, rowdict, replace)

    @classmethod
    def insert_batch(cls, tablename, batch_params, replace=False):
        global key_strs
        value_batch = []
        for param in batch_params:
            keys = param.keys()
            key_strs = ", ".join(["""`%s`""" % key for key in keys])
            value_strs = "(%s)" % ", ".join(
                ["""'%s'""" % "%s" % param.get(key) for key in keys])
            value_batch.append(value_strs)

        sql = """%s INTO %s (%s) VALUES %s""" % (
            "REPLACE" if replace else "INSERT IGNORE", tablename, key_strs, ",".join(value_batch))
        print(sql)
        return cls._instance.execute(sql)

    def update_dict(self, tablename, rowdict, where):
        return self._instance.update_dict(tablename, rowdict, where)

    def transaction(self, query, parameters):
        return self._instance.transaction(query, parameters)

    def get(self, tablename, conds, cols=None, extra_conds=None):
        if extra_conds is None:
            extra_conds = {}
        if cols is None:
            cols = []
        if not tablename:
            return False
        cols = "%s" % ','.join(cols) if cols else '*'
        wheres = []
        values = []
        if conds and isinstance(conds, dict):
            for key, value in conds.items():
                if isinstance(value, (list, tuple)):
                    wheres.append("`%s` IN (%s)" % (key, "'%s'" % "','".join([str(v) for v in value])))
                else:
                    wheres.append("`%s`=%%s" % key)
                    values.append("%s" % value)
        where_str = ' AND '.join(wheres)
        sql = "SELECT {cols} FROM `{tablename}`".format(cols=cols, tablename=tablename)

        if where_str:
            sql += """ WHERE %s """ % where_str
        if extra_conds.get('group_by'):
            sql += """ GROUP by %s """ % ','.join(extra_conds['group_by'])
        if extra_conds.get('order_by'):
            sql += """ ORDER by %s """ % ','.join(extra_conds['order_by'])
        if extra_conds.get('limit'):
            sql += """ LIMIT %s """ % ','.join(map(str, extra_conds['limit']))

        return self._instance.query(sql, *values)

    def _serialize(self, value):
        if isinstance(value, (dict, list, set)):
            value = json.dumps(value)
        else:
            value = "%s" % value
        return value

    def _formatter(self, pairs, delimiter):
        values = []
        for key, value in pairs.items():
            if not isinstance(value, list):
                value = self._serialize(value)
                values.append("""`%s`='%s'""" % (key, value))
            else:
                values.append("""`%s` in ("%s")""" % (key, '","'.join([self._serialize(val) for val in value])))
        return delimiter.join(values)


def error500():
    key = 'error500_mysql'
    return MySQLHelper(
        "%s:%s" % (config.get(key, "host"), config.get(key, "port")),
        config.get(key, "user"),
        config.get(key, "password"),
        config.get(key, "database")
    )
