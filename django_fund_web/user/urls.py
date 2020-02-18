from django.conf.urls import url

from user import views

urlpatterns=[
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^register$',views.register),
    url(r'^check_reg_info$',views.check_reg_info),
]