import math
from django.core.paginator import Paginator
from tools import contains

def get_paging(list_data,pageNum,pageSize=25):
    """
    自定义分页功能
    :param list_data:   数据列表
    :param pageNum:     页数
    :param pageSize:    每页显示最大数量
    :return:        (pages,data)  页面导航对象， 分页的数据。
    """
    pagination = Paginator(list_data, pageSize)
    page = pagination.page(pageNum)
    paging = {}
    paging['next_num'] = page.next_page_number() if page.has_next() else 0
    paging['prev_num'] = page.previous_page_number() if page.has_previous() else 0
    paging['number'] = page.number
    paging['page_size'] = pagination.per_page
    # 需要把pages对象转为列表
    rows = list(pagination.page_range)
    index = 0
    while rows:
        index += 1
        row = rows[:contains.DEFAULT_MAX_PAGE]
        if page.number in row:
            paging['page_range'] = row
            break
        rows = rows[contains.DEFAULT_MAX_PAGE:]
    else:
        paging['page_range'] = None
    paging['page_count'] = pagination.num_pages
    length = math.ceil(pagination.num_pages / contains.DEFAULT_MAX_PAGE)
    if index == 1:
        paging['next_range_num'] = index * contains.DEFAULT_MAX_PAGE + 1
    elif index == length:
        paging['prev_range_num'] = (index - 1) * contains.DEFAULT_MAX_PAGE
    else:
        paging['next_range_num'] = index * contains.DEFAULT_MAX_PAGE + 1
        paging['prev_range_num'] = (index - 1) * contains.DEFAULT_MAX_PAGE
    return paging,page.object_list

class Diy_paginator:

    @staticmethod
    def get_diy_paging(list_data, pageNum, pageSize=15):
        """
        自定义分页功能
        :param list_data:   数据列表
        :param pageNum:     页数
        :param pageSize:    每页显示最大数量
        :return:        (pages,data)  分页对象， 数据对象。
        """
        pagination = Paginator(list_data, pageSize)
        page = pagination.page(pageNum)
        paging = {}
        paging['next_num'] = page.next_page_number() if page.has_next() else 0
        paging['prev_num'] = page.previous_page_number() if page.has_previous() else 0
        paging['number'] = page.number
        paging['page_size'] = pagination.per_page
        paging['total'] = len(list_data)
        paging['page_count'] = pagination.num_pages

        # 把pages对象转为列表
        rows = list(pagination.page_range)
        normal_len = contains.DEFAULT_BOTH_PAGE * 2 + 1
        if len(rows) < normal_len:
            paging['page_range'] =rows
        elif page.number < contains.DEFAULT_BOTH_PAGE:
            paging['page_range'] = rows[:normal_len]
        elif page.number > paging['page_count'] - contains.DEFAULT_BOTH_PAGE:
            paging['page_range'] = rows[paging['page_count'] - normal_len:]
        else:
            paging['page_range'] = rows[page.number - contains.DEFAULT_BOTH_PAGE - 1: page.number + contains.DEFAULT_BOTH_PAGE]

        return paging, page.object_list