# -*- coding: utf-8 -*-
# @Time    : 2019/3/1 上午9:58
# @Author  : yidxue


def create_table_sql(name, cols, types, primaryKeys, comments=None):
    fields = ''
    if comments is not None:
        for col, ctype, comment in zip(cols, types, comments):
            fields += col + " " + ctype + " NOT NULL COMMENT '" + comment + "',"
    else:
        for col, ctype in zip(cols, types):
            fields += col + " " + ctype + " NOT NULL ,"

    sql = """
        CREATE TABLE IF NOT EXISTS `{name}` 
        ({fields} PRIMARY KEY (`{primary}`)) 
        ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
        """.format(name=name, fields=fields, primary=','.join(primaryKeys))

    return sql
