from django.http import HttpResponse
from django.shortcuts import render, redirect

from user.models import User_profile_model


def logging_check(func):
    """
    验证登陆状态
    :param func:
    :return:
    """
    def wrapper(request,*args,**kwargs):
        if "username" in request.session.keys() and "uid" in request.session.keys() :
            pass
        elif "username" in request.COOKIES and "uid" in request.COOKIES:
            try:
                user = User_profile_model.objects.get(username=request.COOKIES["username"])
            except Exception:
                request.delete_cookie('username')
                result = {'code': 10201, 'error': '用户不存在 !!'}
                return HttpResponse(result['error'])
            request.session["username"] = request.COOKIES["username"]
            request.session["uid"] = request.COOKIES["uid"]
            request.session["nickname"] = user.nickname if user.nickname else user.username
            request.session["active"] = user.is_active
        else:
            return redirect("/user/login")

        return func(request,*args,**kwargs)
    return wrapper