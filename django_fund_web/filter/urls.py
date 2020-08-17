from django.conf.urls import url

from filter import views

urlpatterns=[
    url(r'^fundinfo/(?P<code>\w+)$',views.fund_detail_page),
    url(r'^ffpage$',views.fund_filter_page),
    url(r'^queryFund$',views.query_fund),
    url(r'^queryBox/company$',views.query_company),

]