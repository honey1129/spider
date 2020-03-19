#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
@version: python 3.7.0
@author: liuxuchao
@contact: liuxuchao1129@foxmail.com
@software: PyCharm
@file: main.py
@time: 2020-03-14 20:53
"""
from game_info_spider import GameInfoSpider
import game_comment_spider_1
# from multiprocessing import Process
import time



def run():
    GameInfoSpider().run()
    time.sleep(0.5)
    game_comment_spider_1.run()


if not __name__ == 'main':
    run()