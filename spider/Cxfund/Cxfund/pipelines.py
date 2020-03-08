# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class CxfundPipeline(object):
    def process_item(self, item, spider):
        print(item['title'], item['parent_id'], item['lid'])
        return item
