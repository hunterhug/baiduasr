# -*-coding:utf-8-*-
# Created by 一只尼玛 on 16-8-26.
# 功能:
#  文件类

import struct
import os, time, re
import random


# star 找出文件夹下所有xml后缀的文件，可选择递归，选择全路径
def listfiles(rootdir, prefix='.xml', isall=False, iscur=False):
    file = []
    for parent, dirnames, filenames in os.walk(rootdir):
        if parent == rootdir:
            for filename in filenames:
                if filename.endswith(prefix):
                    if isall:
                        file.append(rootdir + '/' + filename)
                    else:
                        file.append(filename)
            if not iscur:
                return file
        else:
            if iscur:
                for filename in filenames:
                    if filename.endswith(prefix):
                        if isall:
                            file.append(rootdir + '/' + filename)
                        else:
                            file.append(filename)
            else:
                pass
    return file


# star 去除标题中的非法字符 (Windows)
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "", title)
    return new_title


# star 递归创建文件夹
def createjia(path):
    try:
        os.makedirs(path)
    except:
        pass
    return path


# star 今天日期的字符串
#     %Y  Year with century as a decimal number.
#     %m  Month as a decimal number [01,12].
#     %d  Day of the month as a decimal number [01,31].
#     %H  Hour (24-hour clock) as a decimal number [00,23].
#     %M  Minute as a decimal number [00,59].
#     %S  Second as a decimal number [00,61].
#     %z  Time zone offset from UTC.
#     %a  Locale's abbreviated weekday name.
#     %A  Locale's full weekday name.
#     %b  Locale's abbreviated month name.
#     %B  Locale's full month name.
#     %c  Locale's appropriate date and time representation.
#     %I  Hour (12-hour clock) as a decimal number [01,12].
#     %p  Locale's equivalent of either AM or PM.
def todaystring(level=3):
    formats = '%Y%m%d'
    if level == 1:
        formats = '%Y'
    elif level == 2:
        formats = '%Y%m'
    elif level == 4:
        formats = '%Y%m%d-%H'
    elif level == 5:
        formats = '%Y%m%d-%H%M'
    elif level == 6:
        formats = '%Y%m%d-%H%M%S'
    else:
        formats = '%Y%m%d'
    today = time.strftime(formats, time.localtime())
    return today


# 文件格式 文件头(十六进制)
# JPEG (jpg) FFD8FF
# PNG (png) 89504E47
# GIF (gif) 47494638
# TIFF (tif) 49492A00
# Windows Bitmap (bmp) 424D
# CAD (dwg) 41433130
# Adobe Photoshop (psd) 38425053
# Rich Text Format (rtf) 7B5C727466
# XML (xml) 3C3F786D6C
# HTML (html) 68746D6C3E
# Email [thorough only] (eml) 44656C69766572792D646174653A
# Outlook Express (dbx) CFAD12FEC5FD746F
# Outlook (pst) 2142444E
# MS Word/Excel (xls.or.doc) D0CF11E0
# MS Access (mdb) 5374616E64617264204A

# 支持文件类型
# 用16进制字符串的目的是可以知道文件头是多少字节
# 各种文件头的长度不一样，少则2字符，长则8字符
def typeList():
    return {
        "FFD8FF": "jpeg",
        "89504E47": "png",
        "47494638": "gif",
        "D0CF11E0": "doc"}


# 字节码转16进制字符串
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()


# star 获取文件类型，传入文件名
def filetype(filename):
    binfile = open(filename, 'br')  # 必需二制字读取
    tl = typeList()
    ftype = 'error'
    for hcode in tl.keys():
        numOfBytes = len(hcode) // 2  # 需要读多少字节
        binfile.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
        hbytes = struct.unpack_from("B" * numOfBytes, binfile.read(numOfBytes))  # 一个 "B"表示一个字节
        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = tl[hcode]
            break
    binfile.close()
    return ftype


# star 文件路径拼接
def filejoin(file=[]):
    s = ""
    for i in file:
        s = s + i + "/"
    return s


# 从文件中读取行，变成列表
def readfilelist(filepath):
    returnlist = []
    try:
        with open(filepath, "rb") as filename:
            namelines = filename.readlines()
            for line in namelines:
                content = line.decode("utf-8", "ignore").replace("\n", "").replace("\r", "")
                if not content:
                    continue
                returnlist.append(content)
    except Exception as err:
        print(err)
        pass
    return returnlist


# 时间函数
def timetochina(longtime, formats='{}天{}小时{}分钟{}秒'):
    day = 0
    hour = 0
    minutue = 0
    second = 0
    try:
        if longtime > 60:
            second = longtime % 60
            minutue = longtime // 60
        else:
            second = longtime
        if minutue > 60:
            hour = minutue // 60
            minutue = minutue % 60
        if hour > 24:
            day = hour // 24
            hour = hour % 24
        return formats.format(day, hour, minutue, second)
    except:
        raise Exception('时间非法')


# 判断文件是否存在
def fileexsit(path):
    return os.path.exists(path)


# 切分文件列表
def devidelist(files, num=0):
    filestype = type(files)
    if not filestype == type([]):
        raise Exception("文件切分只能是列表")
    length = len(files)
    split = {}
    if length <= 0:
        return split
    if num >= length:
        split[0] = files
        return split
    process = length // num
    for i in range(num):
        split[i] = (files[i * process:(i + 1) * process])
    remain = files[num * process:]
    for i in range(len(remain)):
        split[i % num].append(remain[i])
    return split


# 取得URL参数
def geturlattr(url):
    # p/seller/at-a-glance.html/ref=dp_merchant_link?ie=UTF8&seller=AJ11J3FSAZ6XV&isAmazonFulfilled=
    returnmap = {}
    try:
        temp = url.split("?")[1].split("&")
        for i in temp:
            temptemp = i.split("=")
            try:
                returnmap[temptemp[0]] = temptemp[1]
            except:
                pass
    except:
        pass
    return returnmap


# 拼接参数join
def joinany(things, sep=","):
    temp = ""
    for i in range(len(things)):
        if i == len(things) - 1:
            temp = temp + str(things[i])
        else:
            temp = temp + str(things[i]) + sep
    return temp


# 随机数，足够复杂
def allrandom(num):
    try:
        temp = str(os.urandom(num)) + str(os.getpid()) + str(random.randint(0, num - 1))
        random.seed(temp)
        returnd = random.randint(0, num - 1)
    except:
        random.seed()
        returnd = random.randint(0, num - 1)
    # print(returnd)
    return returnd


# 文件批量改名
def renamedir(path, oprefix="md", nprefix="txt"):
    files = listfiles(rootdir=path, prefix=oprefix, isall=True)
    for i in files:
        os.rename(i, i.replace("md", nprefix))


def getroot():
    from os.path import expanduser
    home = expanduser("~")
    # from pathlib import Path
    # home = str(Path.home())
    return home


if __name__ == "__main__":
    # today = time.strftime('%Y%m%d', time.localtime())
    # a = time.clock()
    # print(filejoin(['.', "data", "test"]))
    # print(todaystring(4))
    # b = time.clock()
    # print('运行时间：' + timetochina(b - a))
    #
    # print(fileexsit("///\\\Ge.md"))
    #
    files = [1, 11, 111, 2, 22, 222, 3, 33, 333, 4, 44, 444, 5, 55, 555]
    # print(files)
    print(devidelist(files, 2))
    #
    # print(geturlattr("p/seller/at-a-glance.html/ref=dp_merchant_link?ie=UTF8&seller=AJ11J3FSAZ6XV&isAmazonFulfilled="))
    #
    # print(joinany(files))

    print(getroot())
