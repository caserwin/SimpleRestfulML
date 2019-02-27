#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import router
import tornado.httpserver
import tornado.ioloop
import tornado.locale
import tornado.web
from tornado.options import define, options, parse_command_line
from src.utils import config

port = int(config.get("global", "port"))
debug_mode = int(config.get("global", "server_debug_mode"))
process_num = int(config.get("global", "process_num"))

settings = {
    'debug': debug_mode,
    'template_path': os.getenv("TEMPLATES"),
    'static_path': os.getenv("STATIC"),
    'cookie_secret': 'L8LwECiNRxq2N0N2eGxx9MZlrpmuMEimlydNX/vt1LM='
}

define("port", default=port, help="server listening port")


def set_env():
    cur_dir = sys.path[0]
    os.sys.path.append(os.path.join(cur_dir, "src"))

    os.environ["CONF"] = os.path.join(cur_dir, "conf")
    os.environ["SRC"] = os.path.join(cur_dir, "src")
    os.environ["TEMPLATES"] = os.path.join(cur_dir, "templates")
    os.environ["STATIC"] = os.path.join(cur_dir, "static")


def main():
    parse_command_line()
    print ("start api server at %s" % options.port)

    app = tornado.web.Application(router.url_map, **settings)
    server = tornado.httpserver.HTTPServer(app, max_body_size=800 * 1024 * 1024)
    server.bind(options.port)
    server.start(1 if debug_mode else process_num)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
