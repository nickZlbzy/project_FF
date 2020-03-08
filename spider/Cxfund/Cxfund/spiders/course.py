# -*- coding: utf-8 -*-
import requests
import scrapy
from lxml import etree

from Cxfund.items import CxfundLevelItem


class CourseSpider(scrapy.Spider):
    name = 'course'
    allowed_domains = ['cn.morningstar.com/']
    one_course_url = "http://www.cn.morningstar.com/school/fund/course.aspx?"


    def start_requests(self):
        html = requests.get(url=self.one_course_url).text
        p = etree.HTML(html)
        all_cate = p.xpath('//div[@class="catalog1"]/div')
        item = CxfundLevelItem()
        for cate in all_cate:

            item['parent_id'] = cate.xpath('./@class')[0]
            lis = cate.xpath('./ul/li')
            for li in lis:
                item['title'] = li.xpath('./a/text()')[0]
                item['lid'] = li.xpath('./a/@cat')[0]
                item['url'] = li.xpath('./a/@href')[0]
                print(item['title'])
                yield item


