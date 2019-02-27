# coding:utf-8

from src.handler.base.base_handler import BaseHandler
from src.service.simple_service import SimpleService


class DemoHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(DemoHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        a = int(self.get_argument('a', 1))
        b = int(self.get_argument('b', 1))

        state_code, result = SimpleService(a, b).tranform()

        if state_code == 0:
            self.set_result(result={"result": result})
            return

        elif state_code == 1:
            self.set_result(result={"result": result})
            return

        elif state_code == 2:
            self.set_error(error_code=1, error_message="a is smaller than b")
            return

        # self.set_result(result=result)
