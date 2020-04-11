# -*- coding: utf-8 -*-

import scrapy
from Cxfund.items import CxfundLevelItem, CxfundContentItem
from scrapy_redis.spiders import RedisSpider

class CourseSpider(RedisSpider):
    name = 'course'
    allowed_domains = ['cn.morningstar.com']
    base_url = 'http://www.cn.morningstar.com'
    one_course_url = "http://www.cn.morningstar.com/school/fund/course.aspx?"

    redis_key = 'cxfund:spider'

    def parse(self,response):
        # html = requests.get(url=self.one_course_url).text
        # p = etree.HTML(html)
        all_cate = response.xpath('//div[@class="catalog1"]/div')
        item = CxfundLevelItem()
        for cate in all_cate:

            item['parent_id'] = cate.xpath('./@class').get()
            lis = cate.xpath('./ul/li')

            for li in lis:
                item['title'] = li.xpath('./a/text()').get()
                item['lid'] = li.xpath('./a/@cat').get()
                item['url'] = self.base_url + li.xpath('./a/@href').get()

                yield scrapy.Request(url=item['url'],meta={'item':item},callback=self.get_two)

    def get_two(self,response):
        meta_item1 = response.meta['item']

        list_titles = response.xpath('//div[@class="catalog2"]/a')
        for item in list_titles:
            item_end = CxfundContentItem()
            item_end['lid'] = meta_item1['lid']
            url = item.xpath('./@href').get()
            item_end['url'] = self.base_url +  url
            item_end['title'] = item.xpath('./text()').get()
            yield scrapy.Request(url=item_end['url'],meta={'item':item_end},callback=self.get_content)

    def get_content(self,response):
        item_end = response.meta['item']
        content = response.xpath('//div[@id="course"]//div/div[@class="text"]').extract()
        print(content)