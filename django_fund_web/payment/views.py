import json

from alipay import AliPay
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from tools.utils import Utils

# Create your views here.
from django.views.generic.base import View
import ssl

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
        amount = json_obj.get('amount')
        # fund_id = json_obj.get('fund_id')
        order_id = Utils.get_sync("ali_pay")
        return JsonResponse({'code':200, 'pay_url':self.get_trade_url(order_id, int(amount))})





class OrderResultView(MyAliPay):

    def get(self, request):
        #{'a':['1','2']}
        request_data = {k:request.GET[k] for k in request.GET.keys()}
        print("*" * 45)
        print(request_data)
        print("*" * 45)

        #sign
        sign = request_data.pop('sign')
        is_verify = self.get_verify_result(request_data, sign)
        if is_verify:
            #证明的确是支付宝发过来的
            order_id = request_data.get('out_trade_no')
            #主动查询
            result = self.get_trade_result(order_id)
            if result:
                return redirect("/user/personal")
            else:
                return HttpResponse("支付失败")
        else:
            return redirect("/user/personal")
            # return HttpResponse("系统异常")
