import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from article.mappers import Article_mapper
from system.mappers import Title_url_mapper



def queryBox(request):
    """
    项目字典，加载下拉选
    :param request:
    :return:
    """
    select_name = request.GET.get("selName")
    re_json=Title_url_mapper.query_box(select_name)
    return HttpResponse(json.dumps(re_json))


def queryTopBar(request):
    """
    加载头部导航条
    :param request:
    :return:
    """
    module_name = request.GET.get("moName")
    re_json = Title_url_mapper.query_title_by_module(module_name)
    return HttpResponse(json.dumps(re_json))

def queryTitleByKind(request):
    """
    根据类型加载标题内容
    :param request:
    :return:
    """
    # 前台使用JSON.stringify(dict_obj传参) 则后台用json.loads(request.body)接收
    json_obj = json.loads(request.body)
    kind = json_obj.get("kind")
    value = json_obj.get("value")
    # kind = request.POST.get("kind")
    # value = request.POST.get("value")

    re_data = {}
    # if type == "s1":
    #     re_data = Fund_filter_mapper.query_title_by_name(value)
    #     return re_data
    # elif type == "s2":
    #     re_data = Fund_company_mapper.query_title_by_name(value)
    #     return re_data
    # el
    if kind == "s3":
        re_data = Article_mapper.query_title_by_name(value)
    return HttpResponse(json.dumps(re_data))