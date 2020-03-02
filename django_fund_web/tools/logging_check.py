from django.shortcuts import render, redirect


def logging_check(func):
    """
    验证登陆状态
    :param func:
    :return:
    """
    def wrapper(request,*args,**kwargs):
        if "username" in request.session.keys() and "uid" in request.session.keys():
            pass
        elif "username" in request.COOKIES and "uid" in request.COOKIES:
            request.session["username"] = request.COOKIES["username"]
            request.session["uid"] = request.COOKIES["uid"]
            if "nickname" in request.COOKIES:
                request.session["nickname"] = request.COOKIES["nickname"]
        else:
            return redirect("/user/login")
        return func(request,*args,**kwargs)
    return wrapper