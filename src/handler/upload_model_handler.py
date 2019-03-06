# -*- coding: utf-8 -*-
# @Time    : 2019/3/5 下午4:35
# @Author  : yidxue
from src.handler.base.base_handler import BaseHandler
from src.utils.model_utils import read_model
from tornado.options import options
from src.utils.error import Error
import os

module_path = os.path.abspath(os.path.join(os.curdir))
model_path = os.path.join(module_path, 'model')


class FileUploadHandler(BaseHandler):
    def __init__(self, application, request, **kwargs):
        super(FileUploadHandler, self).__init__(application, request, **kwargs)

    def do_action(self):
        if len(self.request.files) == 0:
            self.set_error(error_code=Error.ERROR_CODE1, error_message="no model file upload")
            return

        max_file_size = 100 * 1024 * 1024
        file_obj = self.request.files['file'][0]
        if len(file_obj["body"]) > max_file_size:
            self.set_error(error_code=Error.ERROR_CODE1, error_message="文件过大, 超过100MB, 上传失败")
            return

        # 存文件
        model_name = file_obj['filename']
        open(os.path.join(model_path, model_name), 'wb').write(file_obj['body'])

        # 更新models全局变量
        model = read_model(os.path.join(model_path, model_name))
        options.models[model_name] = model

        # 返回结果
        self.set_result(result={"message": "upload {file} success!server has reload {model}".format(file=model_name,
                                                                                                    model=model_name)})
