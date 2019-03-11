#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""A lightweight wrapper around MySQLdb.

Originally part of the Tornado framework.  The tornado.database module
is slated for removal in Tornado 3.0, and it is now available separately
as torndb.
"""

from __future__ import absolute_import, division, with_statement

import copy
import logging
import os
import time
from functools import wraps

try:
    import MySQLdb.constants
    import MySQLdb.converters
    import MySQLdb.cursors
except ImportError:
    # If MySQLdb isn't available this module won't actually be useable,
    # but we want it to at least be importable on readthedocs.org,
    # which has limitations on third-party modules.
    if 'READTHEDOCS' in os.environ:
        MySQLdb = None
    else:
        raise

version = "0.3"
version_info = (0, 3, 0, 0)


class RetryCursor(object):
    def __init__(self, conn_obj, core_cursor):
        self._core_cursor = core_cursor
        self._conn = conn_obj

    def __iter__(self):
        return iter(self._core_cursor)

    def __getattr__(self, item):

        origin_attr = getattr(self._core_cursor, item)

        if callable(origin_attr):

            @wraps(origin_attr)
            def _with_retry(*args, **kwargs):
                try:
                    return origin_attr(*args, **kwargs)
                except OperationalError:
                    if self._conn.retry_on_error:
                        logging.warning("error in cursor executing, retrying...", exc_info=1)
                        self._conn.close()
                        self._conn._ensure_connected()
                        self._core_cursor = self._conn._db.cursor()
                        return getattr(self._core_cursor, item)(*args, **kwargs)
                    else:
                        raise

            return _with_retry

        else:
            return origin_attr


def trace_performance(func):
    @wraps(func)
    def _wrap(*args, **kwargs):

        logger = logging.getLogger("performance")
        logger.debug(
            "prepare execute [%s]",
            list((i for i in args if type(i) in [str])).pop(0)[:].replace('\n', ' ')
        )

        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()

        logstr = "[DB] [%s] [%f]" % \
                 (list((i for i in args if type(i) in [str])).pop(0)[:].replace('\n', ' '), te - ts)

        if te - ts >= 0.8:
            logger.error(logstr)
        elif te - ts >= 0.3:
            logger.warning(logstr)
        else:
            logger.info(logstr)

        return result

    return _wrap


class Connection(object):
    """A lightweight wrapper around MySQLdb DB-API connections.

    The main value we provide is wrapping rows in a dict/object so that
    columns can be accessed by name. Typical usage::

        db = torndb.Connection("localhost", "mydatabase")
        for article in db.query("SELECT * FROM articles"):
            print article.title

    Cursors are hidden by the implementation, but other than that, the methods
    are very similar to the DB-API.

    We explicitly set the timezone to UTC and assume the character encoding to
    UTF-8 (can be changed) on all connections to avoid time zone and encoding errors.

    The sql_mode parameter is set by default to "traditional", which "gives an error instead of a warning"
    (http://dev.mysql.com/doc/refman/5.0/en/server-sql-mode.html). However, it can be set to
    any other mode including blank (None) thereby explicitly clearing the SQL mode.
    """

    def __init__(self, host, database, user=None, password=None,
                 max_idle_time=7 * 3600, connect_timeout=0,
                 time_zone="+8:00", charset="utf8", sql_mode="TRADITIONAL", retry_on_error=True):
        self.host = host
        self.database = database
        self.max_idle_time = float(max_idle_time)
        self.retry_on_error = retry_on_error

        args = dict(conv=CONVERSIONS, use_unicode=True, charset=charset,
                    db=database, init_command=('SET time_zone = "%s"' % time_zone),
                    connect_timeout=connect_timeout, sql_mode=sql_mode)
        if user is not None:
            args["user"] = user
        if password is not None:
            args["passwd"] = password

        # We accept a path to a MySQL socket file or a host(:port) string
        if "/" in host:
            args["unix_socket"] = host
        else:
            self.socket = None
            pair = host.split(":")
            if len(pair) == 2:
                args["host"] = pair[0]
                args["port"] = int(pair[1])
            else:
                args["host"] = host
                args["port"] = 3306

        self._db = None
        self._db_args = args
        self._last_use_time = time.time()
        try:
            self.reconnect()
        except Exception:
            logging.error("Cannot connect to MySQL on %s", self.host,
                          exc_info=True)

    def __del__(self):
        self.close()

    def close(self):
        """Closes this database connection."""
        if getattr(self, "_db", None) is not None:
            self._db.close()
            self._db = None

    def reconnect(self):
        """Closes the existing database connection and re-opens it."""
        self.close()
        self._db = MySQLdb.connect(**self._db_args)
        self._db.autocommit(True)

    def iter(self, query, *parameters, **kwparameters):
        """Returns an iterator for the given query and parameters."""
        self._ensure_connected()
        cursor = MySQLdb.cursors.SSCursor(self._db)
        try:
            self._execute(cursor, query, parameters, kwparameters)
            column_names = [d[0] for d in cursor.description]
            for row in cursor:
                yield Row(zip(column_names, row))
        finally:
            cursor.close()

    def strict_iter(self, query, *parameters, **kwparameters):
        """Returns an iterator for the given query and parameters."""
        self._ensure_connected()
        cursor = MySQLdb.cursors.SSCursor(self._db)
        try:
            self._execute(cursor, query, parameters, kwparameters)
            for row in cursor:
                yield row
        finally:
            cursor.close()

    def query(self, query, *parameters, **kwparameters):
        """Returns a row list for the given query and parameters."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            column_names = [d[0] for d in cursor.description]
            return [Row(zip(column_names, row)) for row in cursor]
        finally:
            cursor.close()

    def get(self, query, *parameters, **kwparameters):
        """Returns the (singular) row returned by the given query.

        If the query has no results, returns None.  If it has
        more than one result, raises an exception.
        """
        rows = self.query(query, *parameters, **kwparameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]

    # rowcount is a more reasonable default return value than lastrowid,
    # but for historical compatibility execute() must return lastrowid.
    def execute(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        return self.execute_lastrowid(query, *parameters, **kwparameters)

    def execute_lastrowid(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    def execute_rowcount(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the rowcount from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.rowcount
        finally:
            cursor.close()

    def executemany(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        return self.executemany_lastrowid(query, parameters)

    @trace_performance
    def executemany_lastrowid(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the lastrowid from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.lastrowid
        finally:
            cursor.close()

    @trace_performance
    def executemany_rowcount(self, query, parameters):
        """Executes the given query against all the given param sequences.

        We return the rowcount from the query.
        """
        cursor = self._cursor()
        try:
            cursor.executemany(query, parameters)
            return cursor.rowcount
        finally:
            cursor.close()

    update = execute_rowcount
    updatemany = executemany_rowcount

    insert = execute_lastrowid
    insertmany = executemany_lastrowid

    def gen_update_sql(self, table_name, rowdict, where):
        if not where:
            return False
        update_str = ', '.join(['`%s`=%%s' % k for k in rowdict.keys()])
        values = [v for v in rowdict.values()]
        wheres = []
        for (key, value) in where.items():
            if isinstance(value, tuple) or isinstance(value, list):
                wheres.append("`%s` IN (%%s)" % key)
                values.append(','.join([str(v) for v in value]))
            else:
                wheres.append("`%s`=%%s" % key)
                values.append(value)
        where_str = ' AND '.join(wheres)
        sql = 'UPDATE `%s` SET %s WHERE %s' % (table_name, update_str, where_str)
        return sql, tuple(values)

    def update_dict(self, table_name, rowdict, where):

        sql, values = self.gen_update_sql(table_name, rowdict, where)
        return self.update(sql, *values)

    def gen_insert_sql(self, table_name, rowdict, replace=False):

        allowed_keys = set(row["Field"] for row in self.query("describe %s" % table_name))

        keys = allowed_keys.intersection(rowdict)

        if len(rowdict) > len(keys):
            unknown_keys = set(rowdict) - allowed_keys
            logging.error("skipping keys: %s", ", ".join(unknown_keys))

        columns = ", ".join(['`' + key + '`' for key in keys])
        values_template = ", ".join(["%s"] * len(keys))

        if replace:
            sql = "REPLACE INTO %s (%s) VALUES (%s)" % (
                table_name, columns, values_template)
        else:
            sql = "INSERT INTO %s (%s) VALUES (%s)" % (
                table_name, columns, values_template)

        values = tuple(rowdict[key] for key in keys)

        return sql, values

    def insert_dict(self, table_name, rowdict, replace=False):

        sql, values = self.gen_insert_sql(table_name, rowdict, replace)
        return self.insert(sql, *values)

    def transaction(self, query, parameters):
        cursor = self._cursor()
        self._db.autocommit = False
        status = True
        try:
            for index, sql in enumerate(query):
                cursor.execute(sql, parameters[index])
            self._db.commit()
        except OperationalError as e:
            self._db.rollback()
            logging.error("db trasaction err", exc_info=1)
            raise
        finally:
            cursor.close()
            self._db.autocommit = True

        return status

    def _ensure_connected(self):
        # Mysql by default closes client connections that are idle for
        # 8 hours, but the client library does not report this fact until
        # you try to perform a query and it fails.  Protect against this
        # case by preemptively closing and reopening the connection
        # if it has been idle for too long (7 hours by default).
        if self._db is None:  # (time.time() - self._last_use_time > self.max_idle_time):
            self.reconnect()
        else:
            try:
                self._db.ping()
            except OperationalError:
                logging.getLogger("performance").info(
                    "PING detect DB connection lost, reconnecting, idle time [%f]", time.time() - self._last_use_time
                )
                self.reconnect()

        self._last_use_time = time.time()

    def _cursor(self):
        self._ensure_connected()
        return RetryCursor(self, self._db.cursor())

    @trace_performance
    def _execute(self, cursor, query, parameters, kwparameters):
        try:
            return cursor.execute(query, parameters or kwparameters)
        except OperationalError:
            logging.error("Error connecting to MySQL on %s", self.host, exc_info=1)
            self.close()
            raise


class Row(dict):
    """A dict that allows for object-like property access syntax."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


if MySQLdb is not None:
    # Fix the access conversions to properly recognize unicode/binary
    FIELD_TYPE = MySQLdb.constants.FIELD_TYPE
    FLAG = MySQLdb.constants.FLAG
    CONVERSIONS = copy.copy(MySQLdb.converters.conversions)

    field_types = [FIELD_TYPE.BLOB, FIELD_TYPE.STRING, FIELD_TYPE.VAR_STRING]
    if 'VARCHAR' in vars(FIELD_TYPE):
        field_types.append(FIELD_TYPE.VARCHAR)

    for field_type in field_types:
        CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + [CONVERSIONS[field_type]]

    # Alias some common MySQL exceptions
    IntegrityError = MySQLdb.IntegrityError
    OperationalError = MySQLdb.OperationalError
