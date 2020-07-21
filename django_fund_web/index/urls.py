from django.conf.urls import url

from index import views

urlpatterns = [
    url(r'^$',views.index_page),
    url(r'^index$',views.index_page),
]