from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from article.mappers import Article_mapper
from tools.logging_check import logging_check



def article_course_page(request):

    if request.method == "GET":
        return render(request,"article/article_index.html")


def do_article_info(request,type,artid):
    article_info = Article_mapper.query_by_artId(artid)
    type_name = Article_mapper.get_title_by_type(article_info.get("article_type"))
    return render(request,"article/article_info.html",locals())


def query_title_parent(request,type):
    type = "survey" if type == "art_page" else type
    re_dict = {}
    re_dict['parent_title'] = Article_mapper.query_article_parent()
    list_title = Article_mapper.query_type_article(type)
    list_title_page = Paginator(list_title,2)
    cur_page=request.GET.get('page',1)
    try:
        page =  list_title_page.page(cur_page)
    except Exception as e:
        return HttpResponse("---- page is wrong")


    re_dict['list_title_page'] = list_title_page
    re_dict['page'] = page
    re_dict['type'] = type



    return render(request, "article/article_index.html", re_dict)