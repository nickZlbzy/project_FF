from django.conf.urls import url

from user import views

urlpatterns=[
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^register$',views.register),
    url(r'^check_reg_info$',views.check_reg_info),
    url(r'^mobile_verify$',views.mobile_verify),
    url(r'^personal$',views.personal_center),
    url(r'^evaluation$',views.envaluation),
    url(r'^activation$',views.users_active),
    url(r'^send_email_again$',views.send_email_again),

    url(r'^qq/authorization$',views.OauthQQUrlView.as_view()),
    url(r'^personal/qq_token$',views.OauthQQTokenView.as_view()),

]