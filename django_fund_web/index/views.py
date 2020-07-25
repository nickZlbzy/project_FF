import json

from django.core import serializers
from django.shortcuts import render

from django_redis import get_redis_connection

from article.mappers import Article_mapper
from filter.mappers import Fund_filter_mapper
from tools.contants import *

r = get_redis_connection()

def index_page(request):
    re_data = r.get("index")
    if re_data:
        re_data = json.loads(re_data.decode())
    else:
        left_info=Article_mapper.query_by_kind("article_info",6) # 第二个参数为每个板块显示的文章数量
        courses = Article_mapper.query_article_list2('cls')
        wonder_funds = Fund_filter_mapper.select_wonder_fund()
        re_data = {"left_info":left_info,"courses":courses,"wonder_funds":wonder_funds}
        r.set("index", json.dumps(re_data), INDEX_KEEP_TIME)

    return render(request, "main/index.html", re_data)


