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
            item['title'] = cate.xpath('./span/text()').get()
            item['parent_id'] = 0

            lis = cate.xpath('./ul/li')

            for index,li in enumerate(lis):
                item['url'] = self.base_url + li.xpath('./a/@href').get()
                if index == 0:
                    item['lid'] = cate.xpath('./@class').get()
                    # 第一级分类管道
                    # yield item
                    item['parent_id'] = item['lid']
                item['title'] = li.xpath('./a/text()').get()
                item['lid'] = li.xpath('./a/@cat').get()
                # 分类管道
                # yield item
                yield scrapy.Request(url=item['url'],meta={'item':item},callback=self.get_two)

    def get_two(self,response):
        meta_item1 = response.meta['item']

        list_titles = response.xpath('//div[@class="catalog2"]/a')
        for item in list_titles:
            item_con = CxfundContentItem()

            item_con['lid'] = meta_item1['lid']
            url = item.xpath('./@href').get()
            item_con['article_id'] = url.split('=')[-1]
            item_con['url'] = self.base_url +  url
            item_con['title'] = item.xpath('./text()').get()
            yield scrapy.Request(url=item_con['url'],meta={'item':item_con},callback=self.get_content)

    def get_content(self,response):
        item_con = response.meta['item']
        content = response.xpath('//div[@id="course"]//div/div[@class="text"]').extract()
        # next_url = response.xpath('//div[@id="course"]//div/div[@class="next"]/a/@href').get()
        # item_con['next'] = next_url.split('=')[-1]
        item_con['content'] = content
        # 文章正文管道
        yield item_con