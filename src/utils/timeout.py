#!/usr/bin/python
# -*- coding: utf-8 -*-

import signal
import functools


class TimeoutException(Exception):
    pass


def timeout(seconds, error_message="timeout error, func exec too long"):
    def decorated(func):
        result = [None]

        def _handle_timeout(signum, frame):
            result[0] = error_message
            raise TimeoutException(error_message)

        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)

            try:
                result[0] = func(self, *args, **kwargs)
            finally:
                signal.alarm(0)

            return result[0]

        return wrapper

    return decorated
