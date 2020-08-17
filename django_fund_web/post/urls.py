from django.conf.urls import url

from post import views

urlpatterns = [
    url(r"^home$",views.postHome),
    url(r"^bar/hotBars$",views.query_hot_bar),
    url(r"^bar/(?P<b_code>\w+)$",views.go_into_bar),
    url(r"^publish$",views.publish_theme),

]