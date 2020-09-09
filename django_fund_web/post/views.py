import json


from django.db import transaction
from django.db.models import Max, F
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render


from post.mappers import Post_mapper
from post.models import *
from tools import contains
from tools.paginator import Diy_paginator


def postHome(request):
    if request.method == "GET":
        return render(request,"post/postHome.html")

def query_hot_bar(request):
    list_bar = Post_bar_model.objects.values('name','url').all()[:20]
    data20 = [{'url':item.get('url'),'name':item.get('name')} for item in list_bar]
    re_data = {'code':200,'data':{'data20': data20, 'data3': data20[0:3]}}
    return JsonResponse(re_data)

def query_hot_bars(request,count):
    list_bar = Post_bar_model.objects.values('name','url').all()[:int(count)]
    re_data = {'code':200,
               'data':[{'url':item.get('url'),'name':item.get('name')} for item in list_bar]}
    return JsonResponse(re_data)

def query_home_page(request,cur_page):
    list_titles = Post_mapper.query_home_titles()
    re_data = Diy_paginator.get_diy_paging(list_titles,cur_page)

    return JsonResponse({'code':200,'data':re_data},safe=False)

def query_bar_page(request,b_id,cur_page):
    cur_page=int(cur_page)
    if cur_page<0:
        list_titles = Post_mapper.query_bar_titles(b_id,1)
        cur_page = -cur_page
    else:
        list_titles = Post_mapper.query_bar_titles(b_id)
    re_data = Diy_paginator.get_diy_paging(list_titles,cur_page)

    return JsonResponse({'code':200,'data':re_data},safe=False)



def access_bar(request,b_code):
    if request.method == "GET":
        try:
            bar_info = Post_bar_model.objects.values('bid', 'url', 'name').get(bid=b_code)
        except:
            return render(request,"404.html")

        return render(request, "post/postBar.html", locals())

def publish_theme(request):
    if request.method == "POST":
        if not request.session.get('username'):
            return JsonResponse({'code': 30101, "msg": "请登录！"})
        tid = Utils.get_sync("post_theme")
        post_url = contains.PRE_COMMENT_URL + tid
        max_num = Post_title_model.objects.filter(bar_id=request.POST.get('b_id')).aggregate(
            max_num=Max('sort'))['max_num']
        sort = max_num + 10 if max_num else 10  #sort字段默认从10开始

        theme_info = Post_title_model.objects.create(tid=tid,
                                                     theme=request.POST.get('title'),
                                                     t_content=request.POST.get('content'),
                                                     bar_id=request.POST.get('b_id'),
                                                     url=post_url,
                                                     author=request.session.get('username'),
                                                     sort=sort)
        return JsonResponse({'code':200,"msg":"发表成功!"})

def entrance_theme(request,t_id):
    if request.method == "GET":
        try:
            theme_Info = Post_title_model.objects.get(tid=t_id)
        except:
            return render(request, "404.html")
        return render(request, "post/postComment.html",locals())
    elif request.method == "POST":
        theme_info = Post_mapper.get_theme_info(t_id)

        return JsonResponse({"code":200,"data": theme_info},safe=False)

def query_post_page(request,t_id,cur_page):
    list_comments = Post_mapper.query_theme_comments(t_id)
    re_data = Diy_paginator.get_diy_paging(list_comments, cur_page,12)
    return JsonResponse({"code":200,"data":re_data},safe=False)


def publish_comment(request):
    if request.method == "POST":
        if not request.session.get('username'):
            return JsonResponse({'code': 30101, "msg": "请登录！"})

        revert_to = json.loads(request.POST.get('revert_list'))

        parent_id=0;revert_user=""
        if revert_to:
            parent_id = revert_to[0];revert_user=revert_to[1]
            max_num = Post_comment_model.objects.filter(theme_id=request.POST.get('t_id'),
                        parent_id=revert_to[0]).aggregate(max_num=Max('sort'))['max_num']
        else:
            max_num = Post_comment_model.objects.filter(
                theme_id=request.POST.get('t_id')).aggregate(max_num=Max('sort'))['max_num']
        sort = max_num + 10 if max_num else 10  # sort字段默认从10开始
        with transaction.atomic():
            sid = transaction.savepoint()
            try:
                post_comment = Post_comment_model.objects.create(theme_id=request.POST.get('t_id'),
                                                  content=request.POST.get('content'),
                                                  author=request.session['username'],
                                                  parent_id=parent_id,
                                                  revert_to=revert_user,
                                                  sort=sort,
                                                  equ_type_id=1)
                post_title= Post_title_model.objects.get(tid=request.POST.get('t_id'))
                post_title.comment_count += 1
                post_title.save()
                # Post_title_model.objects.filter(tid=request.POST.get('t_id')).update(
                # comment_count=F('comment_count')+1)

                # 提交事务
                transaction.savepoint_commit(sid)
            except Exception as e:
                print(e)
                transaction.savepoint_rollback(sid)

        return JsonResponse({"code":200,"msg":"评论成功!"})