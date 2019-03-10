#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from configparser import RawConfigParser


class Configuration(object):
    def __init__(self):
        self._config_file = os.path.join("conf", "app.conf")
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
