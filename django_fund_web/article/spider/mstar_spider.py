import random
import re
import time

import requests
from fake_useragent import UserAgent
from lxml import etree


class StarCourseSpider:
    type="cls"
    def __init__(self):
        self.base_url = "http://www.cn.morningstar.com"
        self.home_url="http://www.cn.morningstar.com/school/fund/course.aspx"


    def get_html(self,url):
        html = requests.get(url=url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"}).text
        return html

    def xpath_func(self, html, xbds):
        """解析功能函数"""
        p = etree.HTML(html)
        r_list = p.xpath(xbds)
        return r_list

    def parse_html(self,html,num):
        href_xdbs = "//div[@class='catalog1']/div[@class='level{}']/ul/li/a/@href".format(num)
        list_href1 = self.xpath_func(html, href_xdbs)
        title_xdbs = "//div[@class='catalog1']/div[@class='level{}']/ul/li/a/text()".format(num)
        list_t1 = self.xpath_func(html, title_xdbs)





        for item in list_href1:
            html2 = self.get_html(self.base_url+item)
            href_xdbs2 = "//div[@class='catalog2']/a/@href"
            list_href2 = self.xpath_func(html2,href_xdbs2)
            for href in list_href2:
                html_course = self.get_html(self.base_url+href)
                self.parse_course(html_course,num)
                time.sleep(random.uniform(0,1))

    def parse_course(self,html,num):
        num_xdbs = "//div[@class='catalog1']/div[@class='level{}']/ul/li/a/@num".format(num)
        cat_xdbs = "//div[@class='catalog1']/div[@class='level{}']/ul/li/a/@cat".format(num)
        next_xdbs = "//div[@class='catalog1']/div[@class='level{}']/ul/li/a/@next".format(num)

        list_cat = self.xpath_func(html, cat_xdbs)
        list_num = self.xpath_func(html, num_xdbs)
        list_next = self.xpath_func(html, next_xdbs)
        pattern = re.compile('<div class="areaInner clearfix">.*?<div class="text">(.*?)</div>',re.S)
        text = pattern.findall(html)[0]


    def save_html(self,dict,**kwargs):
        print(dict)







    def run(self):
        html = self.get_html(self.home_url)
        one_title_xdbs = "//div[@class='catalog1']/div/span/text()"
        list_one_title = self.xpath_func(html, one_title_xdbs)
        # sort 暂时从 10开始
        sort01 = 10
        for i in range(1,len(list_one_title)+1):
            # self.parse_html(html,i)
            dict = {}
            dict["parent_id"] = 0
            dict["url"] = '/'
            dict["title"] = list_one_title[i-1]
            dict["module_type"] = 'inv_course'
            dict["course_type"] = 'cls'
            dict["article_id"] = 'cls%s' % i
            dict["sort"] = sort01
            self.save_html(dict, a=1)

            sort01 += 10



if __name__ == '__main__':

    scs = StarCourseSpider()
    scs.run()