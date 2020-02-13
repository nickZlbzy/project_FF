from django.conf.urls import url

from user import views

urlpatterns=[
    url('^loginPage$',views.login_page)
]