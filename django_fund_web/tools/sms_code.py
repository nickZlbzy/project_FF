import json
import random

from django_redis import get_redis_connection
import http.client
import urllib



host = "106.ihuyi.com"
sms_send_uri = "/webservice/sms.php?method=Submit"

class Sms_verify:
    @staticmethod
    def send(phone_num):
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        verify_code = str(int((random.uniform(0,1)*9+1)*100000))

        # 短信验证功能，现在剩余一条了，下面return verify_code语句，会直接输出打印验证码
        return verify_code

        content = "您的验证码是：{}。请不要把验证码泄露给其他人。".format(verify_code)
        conn = http.client.HTTPConnection(host, port=80, timeout=30)

        data = {}
        data['account'] = 'C53200230'
        data['password'] = 'f36214ead573e8fb764aa5a49ea35e37'
        data['mobile'] = phone_num
        data['content'] = content
        data['format'] = 'json'
        params = urllib.parse.urlencode(data)
        # params = urllib.parse.urlencode({'account':'C69687721',
        #      'password':'4c0857b9af197a8243c04bccfd2da77f','mobile':phone_num,
        #          'content':content,'format':'json'})

        conn.request("POST", sms_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()
        json_str = response_str.decode("utf-8")
        re_data=json.loads(json_str)
        if re_data.get('code') == 2:
            return verify_code
        else:
            return None







