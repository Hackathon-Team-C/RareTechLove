from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import url
from .views import RaretechloveappView
#from .views import raretechloveappSearchView

urlpatterns = [
    url(r"sqlbuddy", RaretechloveappView.as_view(), name="sqlbuddy"),
    url(r"", RaretechloveappView.as_view(), name="index"),
    url(r"login", RaretechloveappView.as_view(), name="login"),
    url(r"signup", RaretechloveappView.as_view(), name="signup"),
    url(r"mypage", RaretechloveappView.as_view(), name="mypage"),
    url(r"post", RaretechloveappView.as_view(), name="post"),
    url(r"mukasi", RaretechloveappView.as_view(), name="mukasi"),
    url(r"search", RaretechloveappView.as_view(), name="search"),
    url(r"test", RaretechloveappView.as_view(), name="test"),
] 
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
