#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import tornado.httpserver
import tornado.ioloop
import tornado.locale
import tornado.web
from src.utils import config
from tornado.options import define, options, parse_command_line
# noinspection PyUnresolvedReferences
from src.train.lr_train import LogisticRegressionTrain

port = int(config.get("global", "port"))
debug_mode = int(config.get("global", "server_debug_mode"))
process_num = int(config.get("global", "process_num"))

settings = {
    'debug': debug_mode,
}

define("port", default=port, help="server listening port")


def main():
    parse_command_line()
    print ("start api server at %s" % options.port)

    import router
    app = tornado.web.Application(router.url_map, **settings)
    server = tornado.httpserver.HTTPServer(app, max_body_size=800 * 1024 * 1024)
    server.bind(options.port)
    server.start(1 if debug_mode else process_num)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
