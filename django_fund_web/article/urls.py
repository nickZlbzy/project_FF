from django.conf.urls import url

from article import views

urlpatterns=[
    url(r"^info/(?P<type>\w+)/(?P<artid>\w+)$",views.do_article_info),
    url(r"^info/(?P<type>\w+)$",views.query_title_parent),
    url(r"^course/(?P<level>\w+)/(?P<artid>\w+)$",views.article_course_info),
    url(r"^sendComment$",views.publish_comment),
    url(r"^pressSupport$",views.press_support),
]