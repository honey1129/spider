# “好游快爆”网络爬虫

#### 介绍
“好游快爆“是一家主要发布各种小游戏的信息的网站爬取“好游快爆“网站”排行榜“页面所有TOP100游戏信息并生成info_data.csv文件，利用多线程+队列+生成者消费者模型分别爬取游戏对应的评论信息，并按照”游戏id“+”游戏名“+当前日期形式生成对应评论csv文件。

#### 软件架构

├── Readme.md                   // 说明文档
├── log.py                        // 自定义错误日志生成文件
├── game_comment_spider_1.py         // 游戏评论页爬取
├── game_info_spider.py   //游戏TOP 100信息页爬取
├── main.py                       // 主程序入口



#### 安装教程
无

#### 使用说明

1.直接运行main.py文件即可

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request

