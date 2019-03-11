# coding:utf-8
from src.handler.base.base_handler import BaseHandler
from src.service.compute_service import ComputeService
from src.utils.error import Error


class SimpleComputeHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(SimpleComputeHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        a = int(self.get_argument('a', '1'))
        b = int(self.get_argument('b', '1'))
        ctype = int(self.get_argument('ctype', '0'))
        compute = ComputeService()

        if ctype == 0:
            result = compute.plus(a, b)
            self.set_result(result={"result": result})
            return
        elif ctype == 1:
            result = compute.minus(a, b)
            self.set_result(result={"result": result})
            return
        elif ctype == 2:
            result = compute.multiply(a, b)
            self.set_result(result={"result": result})
            return
        elif ctype == 3:
            if b == 0:
                self.set_error(error_code=Error.ERROR_CODE1, error_message="b can not be 0")
            else:
                result = compute.divide(a, b)
                self.set_result(result={"result": result})
            return
