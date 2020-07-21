from django.conf.urls import url

from system import views

urlpatterns = [
    url(r"^cate/query_box$",views.queryBox),
    url(r"^cate/query_drop_bar$",views.queryTopBar),
    url(r"^cate/query_title_by_kind$",views.queryTitleByKind),
]