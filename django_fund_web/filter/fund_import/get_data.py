import os
import random

import django
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import pymysql

from filter.models import Fund_type, Fund_filter_model

#该爬虫功能django中暂不可用， Scrapy项目制作中




html = 'http://cn.morningstar.com/fundselect/default.aspx'
browser = webdriver.Chrome('/usr/local/bin/chromedriver')
browser.get(html)

# 定义起始页码
page_num = 1

# 连接数据库
connect = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='fund_web', charset='utf8')
cursor = connect.cursor()


class my_fund:
    def __init__(self, f_code=None, f_name=None, f_cat=None, f_level_3=None, f_level_5=None, re_curr_y=None,
                 unit_price=None, day_change=None, is_cpcl=None, is_etqd=None, f_type=None):
        self.f_code = f_code,
        self.f_name = f_name,
        self.f_cat = f_cat,
        self.f_type = f_type
        self.f_level_3 = f_level_3,
        self.f_level_5 = f_level_5,
        self.re_curr_y = re_curr_y,
        self.unit_price = unit_price,
        self.day_change = day_change
        self.is_opcl = is_cpcl
        self.is_etqd = is_etqd


# 爬取共376页
while page_num <= 10:
    # 列表用于存放爬取的数据
    code_list = []  # 基金代码
    name_list = []  # 基金名称
    fund_cat = []  # 基金分类
    fund_eval_3 = []  # 评级（三年）
    fund_eval_5 = []  # 评级（五年）
    return_curr_y = []  # 今年以来汇报（%）
    value1 = []
    value2 = []
    is_oc = []
    is_eq = []
    # 获取每页的源代码
    data = browser.page_source
    # 如果网页没加载完成，则再等待60秒
    if data == None:
        time.sleep(60)
        data = browser.page_source
    # 利用BeautifulSoup解析网页源代码
    bs = BeautifulSoup(data, 'lxml')
    class_list = ['gridItem', 'gridAlternateItem']  # 数据在这两个类下面


    def get_level_3or5(num):
        return int(num) // 2 + 1


    # 取出所有类的信息，并保存到对应的列表里
    for i in range(len(class_list)):
        for tr in bs.find_all('tr', {'class': class_list[i]}):
            tds_text = tr.find_all('td', {'class': "msDataText"})
            tds_nume = tr.find_all('td', {'class': "msDataNumeric"})
            fund_model = my_fund()
            fund_model.f_code = tds_text[0].find_all('a')[0].string
            fund_model.f_name = tds_text[1].find_all('a')[0].string
            fund_model.f_cat = tds_text[2].string
            fund_model.f_level_3 = get_level_3or5(re.search('\d', tds_text[3].find_all('img')[0]['src']).group())
            fund_model.f_level_5 = get_level_3or5(re.search('\d', tds_text[4].find_all('img')[0]['src']).group())
            fund_model.re_curr_y = tds_nume[3].string
            fund_model.unit_price = tds_nume[1].string
            fund_model.day_change = tds_nume[2].string

            fund_model.f_type = Fund_type.objects.values_list('t_id').filter(type_name=fund_model.f_cat)[0]

            fund_model.is_opcl = 1 if re.search("（封闭式）", fund_model.f_cat) or \
                                      re.search(r"\(封闭式\)", fund_model.f_cat) else 2
            if re.search("ETF", fund_model.f_name):
                fund_model.is_etqd = 1
            elif re.search("（QDII）", fund_model.f_name) or re.search(r"\(QDII\)", fund_model.f_name):
                fund_model.is_etqd = 2

            Fund_filter_model.create(f_code=fund_model.f_code,
                                      f_name=fund_model.f_name,
                                      t_type_id=fund_model.f_type,
                                      three_year_level=fund_model.f_level_3,
                                      five_year_level=fund_model.f_level_5,
                                      interest=fund_model.re_curr_y,
                                      unit_price=fund_model.unit_price,
                                      day_change=fund_model.day_change,
                                      is_oc=fund_model.is_opcl,
                                      is_eq=fund_model.is_etqd,
                                      company_id=random.randint(1, 15))

    # 將数据匹配为本地数据库所需要的

    # for i in range(len(fund_cat)):
    #     fund_cat[i] = Fund_type_mapper.get_valid_by_name(fund_cat[i])

    # 找到换页按钮然后点击
    next_page = browser.find_element_by_link_text('>')
    next_page.click()
    page_num += 1
    time.sleep(5)

connect.close()
