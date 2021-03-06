import base64
import random
from urllib.parse import urlencode

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django_fund_web import settings
from tools.sms_code import Sms_verify
from tools.utils import Utils
from .task import send_active_mail
from tools import contains, pro_dict
from tools.logging_check import logging_check

from user.mappers import User_mapper
from user.models import User_profile_model
from django_redis import get_redis_connection
from QQLoginTool.QQtool import OAuthQQ

r = get_redis_connection()

def register(request):
    """
        注册功能
        :param request:
        :return:
    """
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

        password_m = Utils.make_md5s(password)
        try:
            user = User_profile_model.objects.create(username=username,password=password_m,
                            phone=phone,email=email)
        except Exception as e:
            print("register exception:",e)
            re_data = {"code": 10107, "msg": "系统异常!"}
            render(request, "user/register.html", locals())

        # TODO 发送激活邮件
        send_email_verify(username,email)

        request.session["username"] = username
        request.session["uid"] = user.id
    # 重定向到首页（可到个人中心页面提示邮箱验证）
    return redirect("/index")
    # return redirect(reverse('index.views.index_page', args=[]))

def users_active(request):
    """
    处理激活邮件
    :param request:
    :return:
    """
    if request.method != "GET":
        result = {'code':10114,'error':"Please use get"}
    code = request.GET.get('code')
    if not code:
        return HttpResponse(result['error'])
    code_str = base64.urlsafe_b64decode(code.encode())
    new_code_str = code_str.decode()
    username,rcode = new_code_str.split('_')
    print('username:',username)
    old_data =  r.get('email_active:%s'%username)
    if not old_data:
        result = {'code':10115,'error':'Your code is formerly !'}
        return HttpResponse(result['error'])
    if rcode != old_data.decode():
        result = {'code': 10116, 'error': 'Your code is wrong !!'}
        return HttpResponse(result['error'])
    try:
        user = User_profile_model.objects.get(username=username)
    except Exception:
        result = {'code': 10117, 'error': '用户不存在 !!'}
        return HttpResponse(result['error'])
    user.is_active = True
    user.save()
    r.delete('email_active:%s' % username)

    result = {'code': 200, 'msg': "邮箱激活成功！"}
    return redirect("/user/personal")




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



def login(request):
    """
       登陆功能
       :param request:
       :return:
    """
    if request.method == "GET":
        path_from = request.META.get('HTTP_REFERER', '/') ## 记录当前页url
        print(path_from)
        path_from = path_from if path_from != '/user/login' else '/index'
        # 判断是否记住了密码

        if "username" in request.COOKIES and "uid" in request.COOKIES:
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
            return render(request, "user/login.html",re_data)
        password_m = Utils.make_md5s(password)
        if password_m != user.password:

            re_data = {"code": 10108, "msg": "用户名或密码错误!!"}
            return render(request, "user/login.html",re_data)

        request.session["uid"] = user.id
        request.session["username"] = username
        request.session["is_active"] = user.is_active
        nickname = user.nickname
        if nickname:
            request.session["nickname"] = nickname

        try:
            resp = HttpResponseRedirect(request.session['login_from'])
            del request.session['login_from']
        except KeyError as e:
            resp = HttpResponseRedirect("/index")
        # 检查用户是否　勾选了　'记住用户名',如果勾选，还需要在Cookies中存储　uid&username 过期时间为７天
        if 'isSave' in request.POST.keys():
            resp.set_cookie("uid", user.id, contains.COOKIES_KEEP_TIME)
            resp.set_cookie("username", username, contains.COOKIES_KEEP_TIME)
            # resp.set_cookie("is_active", user.is_active, contants.COOKIES_KEEP_TIME)
            # resp.set_cookie("nickname",nickname,contants.COOKIES_KEEP_TIME)
        return resp


def logout(request):
    #登出方法
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    if 'nickname' in request.session:
        del request.session['nickname']
    resp = HttpResponseRedirect('/')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp

def mobile_verify(request):
    if request.method == "GET":
        mobile = request.GET.get("phone")
        if mobile:
            code = Sms_verify.tencent_send(mobile)
            if code:
                key = 'sms:%s'%mobile
                code_m = Utils.make_md5s(code)
                r.set(key,code_m)
                r.expire(key, contains.MOBILE_KEEP_TIME)
                print("本次验证码:",code)
                return JsonResponse({"code":200,"msg":"发送成功！"})
            return JsonResponse({"code": 10109, "msg": "发送失败！"})
    elif request.method == "POST":
        phone = request.POST.get('phone')
        mobile_verify_code = request.POST.get('verifyCode')
        print(phone,mobile_verify_code)
        if mobile_verify_code and len(mobile_verify_code) == 6:
            key = 'sms:%s'%phone
            saved_code = r.get(key).decode()

            verify_code_m = Utils.make_md5s(mobile_verify_code)
            print("saved:", saved_code)
            print(verify_code_m)
            if not saved_code:
                return JsonResponse({"code":10111,"msg":"验证码输入错误"})
            elif saved_code != verify_code_m:
                return JsonResponse({"code":10112,"msg":"验证码输入错误"})

            return JsonResponse({"code": 200})
        else:
            return JsonResponse({"code":10110,"msg":"验证码输入错误!"})

@logging_check
def personal_center(request):
    if request.method == "GET":
        try:
            user = User_profile_model.objects.get(id=request.session['uid'])
        except KeyError as e:
            print(e)
            return redirect('/user/login')

        if user.is_active:
            list_order = user.fund_payment_model_set.all()
            for item in list_order:
                sname = pro_dict.get_from_dict("pay_status", item.status)
                item.status_name = sname if sname else ""

        return render(request,"user/personal.html",locals())
    elif request.method == "POST":
        uid = request.POST.get('uid')
        nickname = request.POST.get('nickname')
        if nickname:
            try:
                user = User_profile_model.objects.get(id=uid)

            except Exception as e:
                print('系统异常，用户不存在')
                return redirect('/user/login')

            user.nickname = nickname
            user.save()
            request.session['nickname'] = nickname
            result = {"code":200,"user":user,"msg":"修改成功!"}
            return render(request, "user/personal.html", result)
        else:
            return render(request, "user/personal.html", {"code":10113})

def envaluation(request):
    if request.method == "GET":
        return render(request,"user/riskEnvaluation.html")
    if request.method == "POST":

        if "uid" not in request.session.keys():
            return redirect("/user/login")
        uid = request.session['uid']
        q1 = request.POST.get("q1")
        q2 = request.POST.get("q2")
        q3 = request.POST.get("q3")
        q4 = request.POST.get("q4")
        q5 = request.POST.get("q5")
        q6 = request.POST.get("q6")
        q7 = request.POST.get("q7")
        q8 = request.POST.get("q8")
        q9 = request.POST.get("q9")
        q10 = request.POST.get("q10")
        q11 = request.POST.get("q11")

        dict1 = {"A": 2, "B": 6, "C": 4, "D": 0}
        dict2_7 = {"A": 0, "B": 2, "C": 4, "D": 6}
        dict8 = {"A": 6, "B": 4, "C": 2, "D": 0}

        # 计算各题分值
        score1 = dict1[q1]
        score2 = dict2_7[q2]
        score3 = dict2_7[q3]
        score4 = dict2_7[q4]
        score5 = dict2_7[q5]
        score6 = dict2_7[q6]
        score7 = dict2_7[q7]
        score8 = dict8[q8]

        # 计算风险承受等级
        risk_bear_score = score1 + score2 + score3 + score4
        # 计算风险偏好等级
        risk_prefer_score = score5 + score6 + score7 + score8
        user = User_profile_model.objects.get(id=uid)
        user.ability = risk_bear_score
        user.preference = risk_prefer_score
        user.save()
        return render(request,"user/personal.html",{"user":user})



def send_email_verify(username,email):
    """
    发送确认邮件
    :param username:
    :param email:
    :return:
    """
    random_num = str(int((random.uniform(0, 1) * 9 + 1) * 1000))
    code_str = username + '_' + random_num
    code_str_bs = base64.urlsafe_b64encode(code_str.encode())
    # 将随机码存储到redis里。 可以存储1-3天
    r.set('email_active:%s' % username, random_num,60*60*24)
    active_url = "http://127.0.0.1:8000/user/activation?code=%s" % (code_str_bs.decode())
    # active_url = "http://www.nickzlbzy.com.cn/user/activation?code=%s" % (code_str_bs.decode())
    # 发邮件
    send_active_mail.delay(email, active_url)

def send_email_again(request):
    if request.method == "GET":
        try:
            user = User_profile_model.objects.get(id=request.session['uid'])
        except KeyError as e:
            print(e)
            return redirect('/user/login')

        if user.is_active:
            return JsonResponse({"code": 10114})
        else:
            send_email_verify(user.username,user.email)
            return JsonResponse({"code": 200,"msg":"发送成功！"})

def get_qq_login_url():
    params = {
        'response_type': 'code',
        'client_id': settings.QQ_CLIENT_ID,
        'redirect_uri': settings.QQ_REDIRECT_URI.encode(),
        'state': settings.QQ_STATE,
        'scope': 'get_user_info',
    }
    return 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(params)

class OauthQQUrlView(View):
    def get(self,request):
        url = get_qq_login_url()
        return JsonResponse({'code': 200, 'oauth_url': url})


class OauthQQTokenView(View):
    """
        用于扫码后接受Authorization Code,通过Authorization Code获取Access Token
        然后通过Access Token获取openid
    """
    def get(self,request):
        # 获取前端传入的code
        code = request.GET.get('code',None)
        print('code:',code)
        if not code:
            return HttpResponse({"code": 10115,'msg':'缺少code'})
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            #使用code向qq请求access_token
            access_token = oauth.get_access_token(code)
            # 使用access_token获取openid
            openid = oauth.get_open_id(access_token)
        except:
            return HttpResponse({"code": 10116,'msg':'qq服务器异常'})

        print('access_token:',access_token)
        print('openid:',openid)
        return JsonResponse({"code": 200, 'msg': 'success!'})