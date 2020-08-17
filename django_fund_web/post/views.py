from django.http import JsonResponse
from django.shortcuts import render

from post.models import Post_bar_model


def postHome(request):
    if request.method == "GET":
        return render(request,"post/postHome.html")

def query_hot_bar(request):
    list_bar = Post_bar_model.objects.values('name','url').all()[:20]
    re_data = {'code':200,
               'data':[{'url':item.get('url'),'name':item.get('name')} for item in list_bar]}
    return JsonResponse(re_data)

def go_into_bar(request,b_code):
    if request.method == "GET":
        try:
            bar_info = Post_bar_model.objects.values('b_code','name').get(b_code=b_code)
        except:
            return render(request,"404.html")

        return render(request, "post/postBar.html", locals())

def publish_theme(request):
    if request.method == "POST":
        print(request.POST)

    return JsonResponse({'code':200})