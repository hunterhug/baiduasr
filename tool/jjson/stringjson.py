# -*-coding:utf-8-*-
# Created by 一只尼玛 on 16-8-12.
# 功能:
#   格式化json字符串


import json


# 格式化json字符串,默认按键排序
def formatStringToString(jstring, sort=True):
    temp = json.loads(jstring)
    temp = json.dumps(temp, indent=4, sort_keys=sort)
    return temp


# 格式化json字符串,并可选择存入文件
def formatStrigToFile(filepath, sort=True, filesavepath=""):
    file = open(filepath, "r")
    jstring = file.read()
    file.close()
    content = formatStringToString(jstring, sort)
    if file != "":
        filesave = open(filesavepath, "w")
        filesave.write(content)
        filesave.close()

    return content
