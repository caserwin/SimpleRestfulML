# -*- coding: utf-8 -*-
# @Time    : 2019/3/5 下午4:35
# @Author  : yidxue

from src.handler.base.base_handler import BaseHandler
from src.utils.error import Error
import os

max_file_size = 100 * 1024 * 1024

module_path = os.path.abspath(os.path.join(os.curdir))
model_path = os.path.join(module_path, 'model')


class FileUploadHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(FileUploadHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        file_dict = self.request.files
        if len(file_dict) == 0:
            self.set_error(error_code=Error.ERROR_CODE1, error_message="no model file upload")
            return

        file_obj = file_dict['file'][0]
        if len(file_obj["body"]) > max_file_size:
            self.set_error(error_code=Error.ERROR_CODE1, error_message="文件过大, 超过100MB, 上传失败")
            return

        # 存文件
        open(os.path.join(model_path, file_obj['filename']), 'wb').write(file_obj['body'])

        self.set_result({"message": "upload file success!"})
