import hashlib

from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django_redis import get_redis_connection

from tools.logging_check import logging_check
from user.mappers import User_mapper
from user.models import User_profile_model



def register(request):
    if request.method == "GET":
        return render(request, "user/register.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        pwd2 = request.POST.get("password")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        if password != pwd2:
            re_data = {"code": 10103, "msg": "两次密码输入不一致"}
            render(request, "user/register.html", locals())
        if User_mapper.check_new(kind="username",value=username):
            re_data = {"code": 10104, "msg": "用户名已存在!"}
            render(request, "user/register.html", locals())
        if User_mapper.check_new(kind="phone",value=phone):
            re_data = {"code": 10105, "msg": "手机号已存在!"}
            render(request, "user/register.html", locals())
        if User_mapper.check_new(kind="username",value=username):
            re_data = {"code": 10106, "msg": "邮箱已存在!"}
            render(request, "user/register.html", locals())

        password_m = make_pwdm(password)
        try:
            user = User_profile_model.objects.create(username=username,password=password_m,
                            phone=phone,email=email)
        except Exception as e:
            print("register exception:",e)
            re_data = {"code": 10107, "msg": "系统异常!"}
            render(request, "user/register.html", locals())

        request.session["username"] = username
        request.session["uid"] = user.id

        print(request.session['uid'])
    # 重定向到首页（可到个人中心页面提示邮箱验证）
    return redirect("/index")
    # return redirect(reverse('index.views.index_page', args=[]))

def check_reg_info(request):
    """
    校验用户名，手机号，邮箱是否存在
    :param request:
    :return: json
    """
    if request.method == "GET":
        kind = request.GET.get("kind")
        value = request.GET.get("value")
        if not value:
            return JsonResponse({"code": 10101})
        result = User_mapper.check_new(kind=kind,value=value)
        if result:
            return JsonResponse({"code": 10102,"msg":"已存在"})

    return JsonResponse({"code":200})


def make_pwdm(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    md5.update(settings.SECRET_SALT.encode())
    return md5.hexdigest()


def login(request):

    if request.method == "GET":
        path_from = request.META.get('HTTP_REFERER', '/')
        # 判断是否记住了密码
        if "username" in request.COOKIES and "uid" in request.COOKIES:
            request.session["username"] = request.COOKIES["username"]
            request.session["uid"] = request.COOKIES["uid"]
            return redirect(path_from)

        request.session["login_from"] = path_from
        return render(request,"user/login.html")
    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User_profile_model.objects.get(username=username)
        except Exception as e:
            re_data = {"code": 10108, "msg": "用户名或密码错误!"}
            render(request, "user/login.html")

        password_m = make_pwdm(password)
        if password_m != password:
            re_data = {"code": 10108, "msg": "用户名或密码错误!!"}
            render(request, "user/login.html")

        request.session["uid"] = user.id
        request.session["username"] = username


        try:
            resp = HttpResponseRedirect(request.session['login_from'])
            del request.session['login_from']
        except KeyError as e:
            resp = HttpResponseRedirect("/")

        # 检查用户是否　勾选了　'记住用户名',如果勾选，还需要在Cookies中存储　uid&username 过期时间为７天
        if 'isSave' in request.POST.keys():
            resp.set_cookie("uid",user.id,60*60*24*7)
            resp.set_cookie("username",username,60*60*24*7)

        return resp


def logout(request):
    #登出
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    resp = HttpResponseRedirect('/')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp
