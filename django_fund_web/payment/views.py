import json

from alipay import AliPay
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from payment.models import Fund_payment_model
from tools.utils import Utils

# Create your views here.
from django.views.generic.base import View
import ssl

from user.models import User_profile_model

ssl._create_default_https_context = ssl._create_unverified_context

app_private_key_string = open(settings.ALIPAY_KEY_DIRS + 'app_private_key.pem').read()
alipay_public_key_string = open(settings.ALIPAY_KEY_DIRS + 'alipay_publick_key.pem').read()


class MyAliPay(View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.alipay = AliPay(
            appid='2016101800717742',
            #订单支付有确切结果后，支付宝请求该地址，汇报结果
            app_notify_url= None,
            app_private_key_string= app_private_key_string,
            alipay_public_key_string= alipay_public_key_string,
            sign_type='RSA2',
            debug=True  # True则将请求发送至沙箱
        )


    def get_trade_url(self, order_id, amount):
        #生成支付地址
        order_string = self.alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,
            total_amount=amount,
            subject=order_id,
            #支付宝跳转前端的显示地址
            # return_url='http://127.0.0.1:8000/user/personal',
            return_url='http://127.0.0.1:8000/payment/result',
            #支付宝服务器post汇报结果
            notify_url='http://127.0.0.1:8000/payment/result'

        )

        return "http://openapi.alipaydev.com/gateway.do?"+ order_string

    def get_verify_result(self, data, sign):
        #验证签名 - True 成功  Fasle 失败
        return self.alipay.verify(data, sign)

    def get_trade_result(self, order_id):
        #给支付宝发http请求，查询订单结果
        result = self.alipay.api_alipay_trade_query(out_trade_no=order_id)
        if result.get('trade_status') == 'TRADE_SUCCESS':
            return True
        return False



class OrderProcessingView(MyAliPay):

    def get(self, request):
        return render(request, 'ajax_alipay.html')

    def post(self, request):
        #获取支付地址
        json_obj = json.loads(request.body)
        price = json_obj.get('price')
        count = json_obj.get('count')
        amount = json_obj.get('amount')
        fund_code = json_obj.get('fund_code')
        order_code = Utils.get_sync("ali_pay")
        print("session_is_active:", request.session["is_active"])
        if not "uid" in request.session:
            return JsonResponse({'code': 20101, 'msg': '请登录!'})
        if not request.session.get('is_active',False):
            user = User_profile_model.objects.filter(uid=request.session['uid'])
            if not user or not user.is_active:
                return JsonResponse({'code': 20103, 'msg': '账号未激活!!'})

        uid = request.session['uid']
        Fund_payment_model.objects.create(order_code=order_code,fund_code=fund_code,
                      price=price,total=count,amount=amount,uid_id=uid)
        return JsonResponse({'code':200, 'pay_url':self.get_trade_url(order_code, int(amount))})



class OrderCountinueView(MyAliPay):

    def get(self, request):
        return render(request, 'ajax_alipay.html')

    def post(self, request):
        #获取支付地址
        json_obj = json.loads(request.body)
        amount = json_obj.get('amount')
        order_code = json_obj.get('order_code')
        if "uid" in request.session:
            uid = request.session['uid']
            return JsonResponse({'code':200, 'pay_url':self.get_trade_url(order_code, int(amount))})
        else:
            return JsonResponse({'code': 20101, 'msg':'请登录!'})




class OrderResultView(MyAliPay):

    def get(self, request):
        #{'a':['1','2']}
        request_data = {k:request.GET[k] for k in request.GET.keys()}

        print(request_data)
        #sign
        sign = request_data.pop('sign')
        # 确认是否是支付宝发过来的
        is_verify = self.get_verify_result(request_data, sign)
        if is_verify:
            #证明的确是支付宝发过来的
            order_id = request_data.get('out_trade_no')
            #主动查询
            result = self.get_trade_result(order_id)
            if result:
                # 确认支付成功后的处理
                fund_order = Fund_payment_model.objects.filter(order_code=order_id)
                if fund_order:
                    fo = fund_order[0]
                    fo.status = 2
                    fo.save()
                return redirect("/user/personal")
            else:
                return HttpResponse("支付失败")
        else:
            return HttpResponse("支付异常")
            # return HttpResponse("系统异常")
