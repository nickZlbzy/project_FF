from django.shortcuts import render, redirect


def logging_check(func):
    def wrapper(request,*args,**kwargs):
        if "username" in request.session.keys() and "uid" in request.session.keys():
            pass
        elif "username" in request.COOKIES and "uid" in request.COOKIES:
            request.session["username"] = request.COOKIES["username"]
            request.session["uid"] = request.COOKIES["uid"]
        else:
            return redirect("/user/login")

        return func(request,*args,**kwargs)
    return wrapper