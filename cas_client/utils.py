# coding: utf-8

'''
author: runforever
'''

import datetime
import sys


def get_datetime(datetime_str, addition_datetime_formats=None):
    default_datetime_formats = [
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d',
    ]

    if addition_datetime_formats:
        default_datetime_formats.extends(addition_datetime_formats)

    for datetime_format in default_datetime_formats:
        try:
            datetime_obj = datetime.datetime.strptime(datetime_str, datetime_format)
            return datetime_obj
        except ValueError:
            continue
    return None


def is_python3():
    """
    是否是python3.x
    :return:
    """
    if sys.version_info >= (3, 0):
        return True
    return False

IS_PYTHON3 = is_python3()
