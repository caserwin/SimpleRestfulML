#!/usr/bin/python
# -*- coding: utf-8 -*-
import simplejson as json
from tornado.web import RequestHandler
from src.utils.timeout import TimeoutException
from src.utils.timeout import timeout


class BaseHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)
        self._status = 0
        self._error_message = ""
        self._result = {}

    def head(self):
        self.run()
        self.do_response()

    def get(self):
        self.run()
        self.do_response()

    def post(self):
        self.run()
        self.do_response()

    def options(self):
        self.run()
        self.do_response()

    def run(self):
        try:
            self.do_action_timeout()
        except TimeoutException:
            self._status = 1
            self._error_message = 'timeout error, func exec too long'
        except Exception as e:
            self._status = 1
            self._error_message = e
            raise e

    # set 600 seconds timeout
    @timeout(600)
    def do_action_timeout(self):
        self.do_action()

    def do_action(self):
        pass

    def do_response(self):
        response = {
            "status": self._status,
        }

        if self._error_message != '':
            self._result["error"] = self._error_message

        response.update(self._result)
        self.write(json.dumps(response))

    def set_result(self, result):
        self._result = result

    def set_error(self, error_code, error_message):
        self._status = error_code
        self._error_message = error_message
