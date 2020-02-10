from django.conf.urls import url

from system import views

urlpatterns = [
    url(r"^cate/query_box$",views.queryBox),

]