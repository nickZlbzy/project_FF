from django_fund_web.celery import app
from django.core.mail import send_mail


@app.task
def send_active_mail(email,code_url):
    subject = '睿选基金激活邮件'
    html_message = '''
        <p>尊敬的用户您好</p>
        <p>激活url为<a href='%s' target='blank'>点击激活</a></p>    
        ''' % code_url
    print(email)
    send_mail(subject=subject, message='', html_message=html_message,
              from_email="732473@qq.com", recipient_list=[email])
