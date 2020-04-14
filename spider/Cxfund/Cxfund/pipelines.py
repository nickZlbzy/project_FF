# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time

import pymysql

from Cxfund.items import CxfundLevelItem,CxfundContentItem
from .settings import *

class CxfundPipeline(object):
    def open_spider(self, spider):
        """爬虫项目启动时，只执行一次，一般用于数据库的链接"""
        self.db = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PWD,
            database=MYSQL_DB,
            charset=MYSQL_CHAR
        )
        self.cursor = self.db.cursor()


    def process_item(self, item, spider):
        if isinstance(item,CxfundLevelItem):

            item['kind']='cls'
            item['module'] = 'inv_course'
            url = item['url'].split('?')[-1]
            ins1 = 'insert into t_article_level(`lid`,`title`,`kind`,`module`,`url`,`parent_id`,' \
                   '`create_time`,`is_active`) value(%s,%s,%s,%s,%s,%s,%s,%s)'

            level = [
                item['lid'],
                item['title'],
                item['kind'],
                item['module'],
                url,
                item['parent_id'],
                time.gmtime(),
                1
            ]

            self.cursor.execute(ins1, level)
            self.db.commit()
        elif isinstance(item,CxfundContentItem):
            ins2 = 'insert into t_article_info(article_id,title,url,content,level_id,' \
                   'create_time,is_active' \
                   ') values(%s,%s,%s,%s,%s,%s,%s)'
            url = '/{lid}/{aid}'.format(lid=item['lid'], aid=item['article_id'])
            content = [
                item['article_id'],
                item['title'],
                url,
                item['content'],
                item['lid'],
                time.gmtime(),
                1
            ]
            print(content)
            self.cursor.execute(ins2, content)
            self.db.commit()



    def close_spider(self, spider):
        """爬虫开始结束时"""
        self.cursor.close()
        self.db.close()

