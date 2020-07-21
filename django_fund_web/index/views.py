from django.shortcuts import render

# Create your views here.
from article.mappers import Article_mapper
from filter.mappers import Fund_filter_mapper


def index_page(request):
    left_info=Article_mapper.query_by_kind("article_info",6) # 第二个参数为每个板块显示的文章数量

    courses = Article_mapper.query_article_list2('cls')
    wonder_funds = Fund_filter_mapper.select_wonder_fund()
    return render(request, "main/index.html",locals())


