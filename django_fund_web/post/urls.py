from django.conf.urls import url

from post import views

urlpatterns = [
    url(r"^home$",views.postHome),
    url(r"^bar/hotBars$",views.query_hot_bar),
    url(r"^bar/hotBars/(?P<count>\d+)$",views.query_hot_bars),
    url(r"^bar/homeThemes/(?P<cur_page>\d+)$",views.query_home_page),
    url(r"^bar/themes/(?P<b_id>\w+)/(?P<cur_page>-?\d+)$",views.query_bar_page),
    url(r"^bars/(?P<b_code>\w+)$",views.access_bar),
    url(r"^themes$",views.publish_theme),
    url(r"^themes/(?P<t_id>\w+)$",views.entrance_theme),
    url(r"^themes/(?P<t_id>\w+)/(?P<cur_page>-?\d+)$",views.query_post_page),
    url(r"^comments$",views.publish_comment),
]