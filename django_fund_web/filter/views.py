import json

from django.core import serializers
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

# Create your views here.

from filter.mappers import Fund_filter_mapper, Fund_company_mapper
from filter.models import Fund_type, Fund_company
from tools.logging_check import logging_check


@logging_check
def fund_filter_page(request):
    type_info = Fund_type.objects.values("t_id","type_name").all()

    return render(request,"fund_filter/filter.html",locals())

def query_fund(request):

    three_grade = request.POST.getlist("three_grade")
    five_grade = request.POST.getlist("five_grade")
    is_oc = request.POST.getlist("is_oc")
    is_eq = request.POST.getlist("is_eq")
    f_type = request.POST.getlist("f_type")
    fund_name = request.POST.get("fund_name")
    company_id = request.POST.get("company_id")




    # 处理筛选器参数
    is_oc = is_oc[0] if len(is_oc) == 1 else None
    five_year_level = five_grade[0] if len(five_grade) == 1 else None
    three_year_level = three_grade[0] if len(three_grade) == 1 else None
    list_fund = Fund_filter_mapper.query_page(five_year_level=five_year_level,
                                              three_year_level=three_year_level,
                                              is_oc=is_oc,
                                              is_eq=is_eq,
                                              f_type=f_type,
                                              f_name=fund_name,
                                              company_id=company_id
                                              # ,page=ser_num
                                              )
    page_size = 25
    pagination = Paginator(list_fund, page_size)

    cur_page = request.POST.get("ser_num",1)
    page = pagination.page(cur_page)

    paging= {}
    paging['next_num'] = page.next_page_number() if page.has_next() else 0
    paging['prev_num'] = page.previous_page_number() if page.has_previous() else 0
    paging['number'] = page.number
    paging['page_size'] = pagination.per_page
    paging['page_range'] = tuple(pagination.page_range)
    re_data=[paging, page.object_list]





    # json_data = serializers.serialize("json",re_dict,ensure_ascii=False)
    re_json = {"code":1,"data":re_data}

    return JsonResponse(re_json,safe=False)

def query_company(request):
    re_json = {"code": 1, "data": Fund_company_mapper.query_box()}

    return JsonResponse(re_json,safe=False)