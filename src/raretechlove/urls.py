from django.conf.urls import url
from .views import RareTechLoveView
#from .views import RareTechLoveAppSearchView

urlpatterns = [
    url(r"", RareTechLoveView.as_view(), name="index"),
    url(r"login", RareTechLoveView.as_view(), name="login"),
    url(r"signup", RareTechLoveView.as_view(), name="signup"),
    url(r"mypage", RareTechLoveView.as_view(), name="mypage"),
    url(r"list", RareTechLoveView.as_view(), name="list"),
]
