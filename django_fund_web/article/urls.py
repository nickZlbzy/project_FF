from django.conf.urls import url

from article import views

urlpatterns=[
    url(r"^(?P<type>\w+)/(?P<artid>\w+)$",views.do_article_info),
    url(r"^(?P<type>\w+)$",views.query_title_parent),
]