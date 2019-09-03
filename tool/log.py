# -*-coding:utf-8-*-
# Created by 一只尼玛 on 2016/10/10.
# 功能:
#   日志类

# CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET

import json
import logging.config
import sys
from tool.jfile.file import *

# 全局变量，是否已经加载配置文件
LOGSUCCESS = False
TODAYTIME = todaystring(3)
# 根目录
BASE_DIR = ""


def setup_logging(default_path='log.json', default_level=logging.INFO, env_key='plog'):
    global LOGSUCCESS
    global BASE_DIR
    if LOGSUCCESS:
        return
    # 当前目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 配置文件位置
    default_path = BASE_DIR + "/config/" + default_path

    path = default_path

    # 从环境变量读取配置文件
    value = os.getenv(env_key)
    if value:
        path = value

    # 配置文件不存在则默认
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
            # 创建日志路径
            logkeepdir = getroot() + "/log/" + todaystring(3)
            # print(logkeepdir)
            try:
                createjia(logkeepdir)
            except:
                pass
            handler = config["handlers"]
            # print(handler)
            for i in handler:
                if "filename" in handler[i].keys():
                    handler[i]["filename"] = logkeepdir + "/" + sys.argv[0].split("/")[-1].replace(".", "") + \
                                             handler[i]["filename"]
        # print(config)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    LOGSUCCESS = True


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.error("errr")
    logger.info("info")
    logger.warning("warn")
    logger.debug("debug")
    # value = os.getenv("path")
    # print(value)
