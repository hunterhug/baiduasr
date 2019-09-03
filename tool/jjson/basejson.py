# -*-coding:utf-8-*-
# Created by 一只尼玛 on 16-8-12.
# 功能:
#
#   序列化和反序列化json
#

import json


# json字符串解析成对象
def stringToObject(jstring):
    return json.loads(jstring)


# json字符串校验是否正确,可打印错误
def isRightJson(jstring, printerror=False):
    try:
        json.loads(jstring)
        if printerror:
            return "", True
        else:
            return True
    except Exception as e:
        if printerror:
            return e, False
        else:
            return False


# 对象解析成json字符串,支持排序和缩进
def objectToString(jobject, sort=False, indent=None):
    return json.dumps(jobject, sort_keys=sort, indent=indent)
