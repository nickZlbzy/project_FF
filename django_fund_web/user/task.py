import json
import random
import urllib

from django_fund_web.celery import app
from django.core.mail import send_mail


@app.task
def send_active_mail(email,code_url):
    subject = '睿选基金激活邮件'
    html_message = '''
        <p>尊敬的用户您好</p>
        <p>激活url为<a href='%s' target='blank'>点击激活</a></p>    
        ''' % code_url
    send_mail(subject=subject, message='', html_message=html_message,
              from_email="732473@qq.com", recipient_list=[email])

# """
# 互亿无线短信验证功能
# """
# host = "106.ihuyi.com"
# sms_send_uri = "/webservice/sms.php?method=Submit"
# @app.task
# def send_short_verify(phone_num):
#     headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#     verify_code = str(int((random.uniform(0,1)*9+1)*100000))
#     # 短信验证功能，现在剩余一条了，下面return verify_code语句，会直接输出打印验证码
#     print('verify_code:',verify_code)
#     return verify_code
#
#     content = "您的验证码是：{}。请不要把验证码泄露给其他人。".format(verify_code)
#     conn = http.client.HTTPConnection(host, port=80, timeout=30)
#
#     data = {}
#     data['account'] = 'C53200230'
#     data['password'] = 'f36214ead573e8fb764aa5a49ea35e37'
#     data['mobile'] = phone_num
#     data['content'] = content
#     data['format'] = 'json'
#     params = urllib.parse.urlencode(data)
#     conn.request("POST", sms_send_uri, params, headers)
#     response = conn.getresponse()
#     response_str = response.read()
#     conn.close()
#     json_str = response_str.decode("utf-8")
#     re_data=json.loads(json_str)
#     if re_data.get('code') == 2:
#         return verify_code
#     else:
#         return None
