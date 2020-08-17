import json
import math

from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.

from filter.mappers import Fund_filter_mapper, Fund_company_mapper
from filter.models import Fund_type, Fund_company
from tools.get_pagination import get_pagination

from tools.logging_check import logging_check



def fund_detail_page(request,code):
    # code = request.GET.get("code")
    fund_info = Fund_filter_mapper.select_fund_by_code(code)
    if fund_info:
        return render(request,"fund_info/fund_info.html",locals())



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



def query_company(request):
    """
    加载公司下拉选
    :param request:
    :return:
    """
    re_json = {"code": 1, "data": Fund_company_mapper.query_box()}

    print()
    return JsonResponse(re_json,safe=False)