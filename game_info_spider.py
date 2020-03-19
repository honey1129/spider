#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
@version: python 3.7.0
@author: liuxuchao
@contact: liuxuchao1129@foxmail.com
@software: PyCharm
@file: new_game.py
@time: 2020-03-09 16:31
"""
import csv
import requests
from lxml import etree
import log
import re



class GameInfoSpider():


    def __init__(self):
        self.headers ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0',
        }
        self.info_list = []

    # 发送请求获取首页游戏信息get(
    def send_requests(self,url='https://www.3839.com/top/hot.html'):
        response = requests.get(url,headers= self.headers ).content.decode('utf-8')
        return response

    # 发送二次json请求获取评论数据
    def send_comment_request(self,url):
        json_response = requests.get(url,headers = self.headers).json()
        comment_num =json_response['num']
        return comment_num

    # 解析info网页信息
    def info_parse_data(self,parse_data):
        data = etree.HTML(parse_data)
        li_list = data.xpath('/html/body/div[1]/div[4]/ul/li')
        # 循环li_list并存入data_list中,数据量过大可使用迭代器
        for li in li_list:
            data_dic = {}
            data_dic['game_id'] = re.search(r"a/(\d+).htm",li.xpath('.//a/@href')[0]).group(1)
            data_dic['game_name'] = li.xpath('.//div[1]/em/a/text()')[0]
            data_dic['logo'] = 'https:'+li.xpath('./a/img[@class="gameLogo"]/@lz_src')[0]
            data_dic['introduce'] = li.xpath('.//div[1]/p[2]/text()')[0]
            data_dic['score'] = li.xpath('.//div[1]/div[1]/div/span/text()')[0][:-1]
            try:
                # 此处两种方法去获取comment数量:1.获取评论json数据，2.解析游戏详情页评论tag信息
                # comment_url = 'https://www.3839.com/cdn/comment/view_v2-ac-json-pid-1-fid-'+str(data_dic['game_id'])+'\
                # -p-1-order-1-htmlsafe-1-urltype-1-audit-1.htm'
                # data_dic['comment_count'] = self.send_comment_request(comment_count)
                data_dic['comment_count'] = etree.HTML(self.send_requests(url = 'https:'+ str(li.xpath('.//a/@href')[0]))).\
                xpath('/html/body/div[1]/div[3]/div[1]/div[1]/div[2]/a[2]/span/text()')[0]
            except Exception as e:
                log.MyLog().error(e)#使用logging模块记录发生的错误信息并生成日志文件
                data_dic['comment_count'] = ''
            data_dic['tag'] = li.xpath('.//div[1]/div[2]/div/span[1]/a/text()')[0]+'、'\
                              + li.xpath('.//div[1]/div[2]/div/span[2]/a/text()')[0]+'、'+li.xpath('.//div[1]/div[2]/div/span[3]/a/text()')[0]
            data_dic['ranking'] = li.xpath('./span[contains(@class,"rank-num")]/text()')[0]
            self.info_list.append(data_dic)

    # 下载数据(csv格式)
    def download_data(self):
        with open('info_data.csv', 'w',newline='',encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(self.info_list[0].keys())
            for data_dic in self.info_list:
                writer.writerow(data_dic.values())

    # 统筹调用
    def run(self):
        self.info_parse_data(self.send_requests())
        self.download_data()
        print("共抓取到%s条数据" % len(self.info_list))


if __name__ == '__main__':
    GameInfoSpider().run()


