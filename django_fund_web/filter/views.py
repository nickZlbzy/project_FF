import json
import math

from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.

from filter.mappers import Fund_filter_mapper, Fund_company_mapper
from filter.models import Fund_type, Fund_company
from tools.contants import DEFAULT_MAX_PAGE
from tools.logging_check import logging_check


@logging_check
def fund_filter_page(request):
    """
       基金筛选器模块
    :param request:
    :return:
    """
    type_info = Fund_type.objects.values("t_id","type_name").all()
    return render(request,"fund_filter/filter.html",locals())

def query_fund(request):
    """
        基金筛选方法
    :param request:
    :return:
    """
    three_grade = request.POST.getlist("three_grade")
    five_grade = request.POST.getlist("five_grade")
    is_oc = request.POST.getlist("is_oc")
    is_eq = request.POST.getlist("is_eq")
    f_type = request.POST.getlist("f_type")
    fund_name = request.POST.get("fund_name")
    company_id = request.POST.get("company_id")
    cur_page = request.POST.get("ser_num", 1)
    # 处理筛选器参数
    is_oc = is_oc[0] if len(is_oc) == 1 else None
    five_year_level = five_grade[0] if len(five_grade) == 1 else None
    three_year_level = three_grade[0] if len(three_grade) == 1 else None

    list_fund = Fund_filter_mapper.query_list(five_year_level=five_year_level,
                                              three_year_level=three_year_level,
                                              is_oc=is_oc,
                                              is_eq=is_eq,
                                              f_type=f_type,
                                              f_name=fund_name,
                                              company_id=company_id)
                                              # ,page=ser_num
    re_data = get_pagination(list_fund,cur_page)
    re_json = {"code":1,"data":re_data}
    return JsonResponse(re_json,safe=False)

def get_pagination(list_data,pageNum,pageSize=25):
    """
    自定义分页页码对象
    :param list_data:   数据列表
    :param pageNum:     页数
    :param pageSize:    每页显示最大数量
    :return:        (pages,data)
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
        row = rows[:DEFAULT_MAX_PAGE]
        if page.number in row:
            paging['page_range'] = row
            break;
        rows = rows[DEFAULT_MAX_PAGE:]
    else:
        paging['page_range'] = None
    paging['page_count'] = pagination.num_pages
    length = math.ceil(pagination.num_pages / DEFAULT_MAX_PAGE)
    if index == 1:
        paging['next_range_num'] = index * DEFAULT_MAX_PAGE + 1
    elif index == length:
        paging['prev_range_num'] = (index - 1) * DEFAULT_MAX_PAGE
    else:
        paging['next_range_num'] = index * DEFAULT_MAX_PAGE + 1
        paging['prev_range_num'] = (index - 1) * DEFAULT_MAX_PAGE
    return paging,page.object_list

def query_company(request):
    """
    加载公司下拉选
    :param request:
    :return:
    """
    re_json = {"code": 1, "data": Fund_company_mapper.query_box()}

    return JsonResponse(re_json,safe=False)