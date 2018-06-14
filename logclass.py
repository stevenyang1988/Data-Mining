import logging
import sys
from functools import wraps


class Log(object):

    @staticmethod
    def _get_caller():
        file_name = sys._getframe(2).f_code.co_filename
        line_no = sys._getframe(2).f_lineno
        func_name = sys._getframe(2).f_code.co_name

        return file_name, line_no, func_name

    @staticmethod
    def _log(my_logger, file_name, line_no, func_name, message):
        my_logger('[{0}:{1}] [{2}] {3}'.format(file_name, line_no, func_name, message))

    @staticmethod
    def critical(message):
        file_name, line_no, func_name = Log._get_caller()
        Log._log(logging.critical, file_name, line_no, func_name, message)

    @staticmethod
    def error(message):
        file_name, line_no, func_name = Log._get_caller()
        Log._log(logging.error, file_name, line_no, func_name, message)

    @staticmethod
    def warning(message):
        file_name, line_no, func_name = Log._get_caller()
        Log._log(logging.warning, file_name, line_no, func_name, message)

    @staticmethod
    def info(message):
        file_name, line_no, func_name = Log._get_caller()
        Log._log(logging.info, file_name, line_no, func_name, message)

    @staticmethod
    def debug(message):
        file_name, line_no, func_name = Log._get_caller()
        Log._log(logging.debug, file_name, line_no, func_name, message)

    @staticmethod
    def trace_log():
        def _trace_log(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                file_name, line_no, func_name = Log._get_caller()

                logging.info('[{0}:{1}] [{2}] <{3}> start'.format(file_name, line_no, func_name, func.__name__))
                out = func(*args, **kwargs)
                logging.info('[{0}:{1}] [{2}] <{3}> end'.format(file_name, line_no, func_name, func.__name__))

                return out
            return wrapper
        return _trace_log


# global function
trace_log = Log.trace_log
