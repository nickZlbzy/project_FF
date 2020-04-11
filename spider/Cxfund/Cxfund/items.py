# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CxfundLevelItem(scrapy.Item):
    # define the fields for your item here like:
    lid = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    # kind = scrapy.Field()
    # module = scrapy.Field()
    parent_id = scrapy.Field()

class CxfundContentItem(scrapy.Item):
    article_id  = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    author = scrapy.Field()
    next = scrapy.Field()
    lid = scrapy.Field()