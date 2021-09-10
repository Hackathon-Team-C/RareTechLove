from django.contrib import admin
from django.urls import path

from django.conf.urls import url
from .views import RaretechloveappView
#from .views import raretechloveappSearchView

urlpatterns = [
    url(r"sqlbuddy", RaretechloveappView.as_view(), name="sqlbuddy"),
    url(r"", RaretechloveappView.as_view(), name="index"),
    url(r"login", RaretechloveappView.as_view(), name="login"),
    url(r"signup", RaretechloveappView.as_view(), name="signup"),
    url(r"mypage", RaretechloveappView.as_view(), name="mypage"),
]
