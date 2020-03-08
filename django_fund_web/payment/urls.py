from django.conf.urls import url

from payment import views

urlpatterns=[

    url(r'^jump/', views.OrderProcessingView.as_view()),
    url(r'^jump2/', views.OrderCountinueView.as_view()),
    url(r'^result/', views.OrderResultView.as_view())
]