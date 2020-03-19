#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
@version: python 3.7.0
@author: liuxuchao
@contact: liuxuchao1129@foxmail.com
@software: PyCharm
@file: log.py
@time: 2020-03-10 10:11
"""

import logging
import os.path
import time


class MyLog():
    '''此类用于创建自己的log'''
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
        log_path = os.path.dirname(os.getcwd()) + '/Logs/'#需先创建Logs文件夹
        log_name = log_path + rq + '.log'
        logfile = log_name
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        # 创建一个handler，用于写入日志文件和控制台
        fh = logging.FileHandler(logfile, mode='w')
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)  # 输出到console的log等级的开关
        # 定义handler的输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 将logger添加到handler里面
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

# 日志
    def debug(self,msg):
        self.logger.debug(msg)
    def warning(self, msg):
        self.logger.warning(msg)
    def error(self, msg):
        self.logger.error(msg)
    def critical(self, msg):
        self.logger.critical(msg)