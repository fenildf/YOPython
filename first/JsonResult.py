# -*- coding:utf-8 -*-
import json

__author__ = 'striveliu'


def convert_to_builtin_type(obj):
    """
    json convert fun
    """
    d = {}
    d.update(obj.__dict__)
    return d


class ApiCommonResult(object):
    """
    API 返回结果通用定义
    """

    def __init__(self, data, name="", count=0, success=False, code='API_10001', msg=None, api_version='1.0',cTime=0):
        self.name = name
        self.data = data
        self.success = success
        self.code = code
        self.msg = msg
        self.api_version = api_version
        if cTime != 0:
            self.currentTime = cTime
        if data:
            self.count = count
            self.success = True
            self.count = len(data)
        else:
            self.success = False

    def to_json(self):
        return json.dumps(self, default=convert_to_builtin_type)