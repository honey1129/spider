#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
@version: python 3.7.0
@author: liuxuchao
@contact: liuxuchao1129@foxmail.com
@software: PyCharm
@file: game_comment_spider_1.py
@time: 2020-03-17 21:31
"""
import log
import pandas as pd
import time
import csv
import threading
from queue import Queue
import re
import requests
import os


# 向first_url_queue中添加所有信息的元组形式
def first_url_process(first_url_queue):
    df = pd.read_csv('info_data.csv')
    final_df = df[df['comment_count'].notnull()]
    final_data_df = final_df.loc[:, ('game_id', 'game_name', 'comment_count')]
    data_list = [tuple(x) for x in final_data_df.values]
    for tuple1 in data_list:
        first_url_queue.put(tuple1, block = False)

#构建评论信息请求url并将url,game_id,game_name以字典形式放入队列
class FirstUrlConsumer(threading.Thread):
    def __init__(self, first_url_queue, final_url_queue, ):
        threading.Thread.__init__(self)
        self.__first_url_queue = first_url_queue
        self.__final_url_queue = final_url_queue

    # 重写run方法。
    def run(self):
        print('first_url_process' + str(threading.currentThread().ident) + '线程开始工作')
        while True:
            if not self.__first_url_queue.empty():
                comment_dic = {}
                data_tuple = self.__first_url_queue.get(block = False)#以非阻塞方式取
                self.__first_url_queue.task_done()
                game_id = data_tuple[0]#取出游戏id
                game_name = data_tuple[1]#取出游戏姓名
                comment_count = data_tuple[2]#取出评论count数
                comment_url_list = []
                for i in range(1, 101 if ((int(comment_count) // 10) > 100) else ((int(comment_count) // 10) + 1)):
                    comment_url = 'https://www.3839.com/cdn/comment/view_v2-ac-json-pid-1-fid-' + str(game_id) + '-p-' + str(i) + '-order-1-htmlsafe-1-urltype-1-audit-1.htm'
                    comment_url_list.append(comment_url)
                comment_dic['game_id'] = game_id
                comment_dic['game_name'] = game_name
                comment_dic['comment_url_list'] = comment_url_list
                self.__final_url_queue.put(comment_dic,block =False)
            else:
                print('first_url_process' + str(threading.currentThread().ident) + '线程工作结束')
                break

# 构造解析数据生产者线程。
class DataProducess(threading.Thread):
    def __init__(self, final_url_queue, data_queue):
        threading.Thread.__init__(self)  # 继承父类属性
        self.__url_queue = final_url_queue  # 评论url线程的队列
        self.__data_queue = data_queue #解析数据线程队列
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        }  # 默认请求头

    #重写父类run方法
    def run(self):
        print('data_process' + str(threading.currentThread().ident) + '线程开始工作')
        while True:
            if not self.__url_queue.empty():
                comment_dic = self.__url_queue.get(block = False)
                self.__url_queue.task_done()
                comment_url_list= comment_dic['comment_url_list']
                game_id = comment_dic['game_id']
                game_name = comment_dic['game_name']
                comment_all_data_dic = {}
                comment_all_content_list = []
                for comment_url in comment_url_list:
                    comment_content_dic = {}
                    n = 3  # 设置三次请求json数据的次数，若三次出错，则使用自定义log模块记录错误信息
                    while n > 0:
                        try:
                            response = requests.get(comment_url, headers=self.headers, timeout=3).json()
                        except Exception as e:
                            log.MyLog().error(e)#使用自定义模块捕捉异常
                            n -= 1
                        else:
                            content_list = response['content']
                            for comment_content in content_list:
                                comment_content_dic['comment_id'] = comment_content['id']
                                comment_content_dic['user_id'] = comment_content['uid']
                                comment_content_dic['username'] = comment_content['username']
                                comment_content_dic['portrait'] = 'https://'+comment_content['avatar'][4:]
                                comment_content_dic['creat_time'] = comment_content['time']
                                comment_content_dic['content'] = comment_content['comment']
                                try:
                                    comment_content_dic['reply_count'] = len(comment_content['reply'])
                                except Exception as e:
                                    comment_content_dic['reply_count'] = 0
                                else:
                                    comment_content_dic['reply_count'] = len(comment_content['reply'])
                            comment_all_content_list.append(comment_content_dic)
                            break
                comment_all_data_dic['game_id'] = game_id
                comment_all_data_dic['game_name'] = game_name
                comment_all_data_dic['game_comment_list'] = comment_all_content_list
                self.__data_queue.put(comment_all_data_dic, block = False)
            else:
                print('data_process' + str(threading.currentThread().ident) + '线程工作完成')
                break


class DataDownLoad(threading.Thread):


    def __init__(self, data_queue):
        threading.Thread.__init__(self)
        self.__data_queue = data_queue
        self.path =os.path.join(os.getcwd(),'评论信息')

    # def path(self):
    #     # 如果不存在“评论信息”文件夹就创建
    #     if not os.path.exists(self.path):
    #         os.mkdir('评论信息')
    def run(self):
        if not os.path.exists(self.path):
            os.mkdir('评论信息')
        print('down_process' + str(threading.currentThread().ident) + '线程开始工作')
        while True:
            # if not self.__data_queue.empty():
            #使用阻塞操作超时60自动退出循环方式结束循环
            try:
                data = self.__data_queue.get(block = True ,timeout= 60 )
            except Exception as e:
                break
            else:
                self.__data_queue.task_done()
                game_id = data['game_id']
                game_name = data['game_name'].replace(':','-')
                game_comment_list= data['game_comment_list']
                date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                with open(self.path+'\\\\'+str(game_id)+str(game_name)+str(date) + '最新评论.csv', 'w', newline='', encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(game_comment_list[0].keys())
                    for game_comment in game_comment_list:
                        writer.writerow(game_comment.values())
                print('down_process' + str(threading.currentThread().ident) + '线程工作完成')
# 统筹调用
def run():
    first_url_queue = Queue()
    final_url_queue = Queue()
    data_queue = Queue()
    first_url_process(first_url_queue)

# 此段为测试代码，
# while True:
#     data = first_url_queue.get()
#     first_url_queue.task_done()
#     if not first_url_queue.empty():
#         print(data)
#     else:
#         break
    thread_list = []
    for i in range(3):
        t = FirstUrlConsumer(first_url_queue,final_url_queue)
        t.daemon = True
        t.start()
        # thread_list.append(t)
    for i in range(25):
        t = DataProducess(final_url_queue, data_queue)
        t.daemon = True
        t.start()
        # thread_list.append(t)
    # while True:
    #     if not data_queue.empty():
    #         data = data_queue.get()
    #         data_queue.task_done()
    #         print(data)
    #     else:
    #         break
    for i in range(10):
        t = DataDownLoad(data_queue)
        t.daemon = True
        t.start()
        thread_list.append(t)
    for queue in [first_url_queue,final_url_queue,data_queue]:
        queue.join()
    for thread in thread_list:
        thread.join()
    print('全部评论信息已采集完毕')

if __name__ == '__main__':
    run()

