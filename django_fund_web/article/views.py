import time

from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from article.mappers import Article_mapper
from django_redis import get_redis_connection
from tools import contants

r = get_redis_connection('likes')


def article_course_info(request,level,artid):
    """
    投资学堂， test
    :param request:
    :return:
    """
    if request.method == "GET":
        # print("session_is_active:", request.session["is_active"])
        level = None if level == 'index' else level
        data = Article_mapper.query_cls_all(level)
        info = ""
        if artid != "0":
            for item in data[1]:
                if item.article_id == artid:
                    info = item
                    break
        else:
            info = data[1][0]

        re_dict = {'right_titles':data[0],'left_titles':data[1],'info':info,
                   'level':level,'artid':artid}

        return render(request,"article/course_page.html",re_dict)


def do_article_info(request,type,artid):
    """
    文章内容显示
    :param request:
    :param type:
    :param artid:
    :return:
    """
    article_info = Article_mapper.select_by_artId(artid)
    type_info = Article_mapper.get_title_by_lid(article_info.get("level_id"))
    print(type_info.get('url'))
    # 获取点赞信息
    like_count =  r.hget('all_like_count',artid)
    like_count = int(like_count.decode()) if like_count else 0
    uname = request.session.get('username',None)
    result = None
    if uname and like_count > 0:
        key_au = artid + '::' + uname
        result = r.hget('user_like_article',key_au)
        result = result.decode() if result else 0

    return render(request,"article/article_info.html",locals())


def query_title_parent(request,type):
    """
   文章模块首页
   :param request:
   :param type:
   :param artid:
   :return:
   """

    level_id = "survey" if type == "art_page" else type
    re_dict = {}
    re_dict['parent_title'] = Article_mapper.query_article_parent()
    print(re_dict['parent_title'][0])
    list_title = Article_mapper.query_type_article(level_id)
    list_title_page = Paginator(list_title,12)
    cur_page=request.GET.get('page',1)
    try:
        page =  list_title_page.page(cur_page)
    except Exception as e:
        return HttpResponse("---- page is wrong")

    re_dict['list_title_page'] = list_title_page
    re_dict['page'] = page
    re_dict['type'] = level_id

    return render(request, "article/article_index.html", re_dict)

def publish_comment(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        if not comment:
            print(type(comment))

    return HttpResponse("")

def press_support(request):
    uname = request.session.get('username')
    if not uname:
        re_data = {'code':-1,'msg':'请登录！'}
        return JsonResponse(re_data)
    
    article_id = request.GET.get('artid')
    key_au = article_id + '::' + uname
    count = r.hget('article_like_count',key_au)

    status = r.hget('user_like_article',key_au)
    status = status.decode() if status else None
    print(status)
    code = None
    # status存在三种情况 None 0 1
    if not status or status == '0':
        # 设置点赞状态
        r.hset('user_like_article',key_au,contants.LIKE_STATUS)
        # 点赞数自增1
        r.hincrby('all_like_count',article_id,1)
        code = 1
    else:
        r.hset('user_like_article', key_au, contants.LIKE_CANCEL_STATUS)
        r.hincrby('all_like_count', article_id, -1)
        code = 0

    re_data = {'code':code,'count':r.hget('all_like_count',article_id).decode()}
    return JsonResponse(re_data)



    
