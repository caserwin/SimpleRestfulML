#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from ConfigParser import RawConfigParser


class Configuration(object):
    def __init__(self, config_file=None):
        user = os.getenv("USER") or "app"
        default_conf = os.path.join(os.getenv("CONF") or "conf", user + ".conf")

        if not os.path.exists(default_conf):
            dir_name = os.path.dirname(default_conf)
            default_conf = os.path.join(dir_name, "app.conf")

        self._config_file = default_conf if not config_file else config_file
        self._load()

    def _load(self):
        self._config = RawConfigParser()
        self._config.read(self._config_file)

    def get_section(self, section):
        if self._config.has_section(section):
            return dict(self._config.items(section))

        return {}

    def get(self, section, option):
        return self._config.get(section, option)


def get_section(section):
    return Configuration().get_section(section)


def get(section, option):
    return Configuration().get(section, option)
