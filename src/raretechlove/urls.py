from django.urls import path
from .views import Top,Login,SignUp,Logout, Top,Mypage
#from .views import RareTechLoveAppSearchView

urlpatterns = [
    path('', Top.as_view(), name='index'),
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("signup/", SignUp.as_view(), name="signup"),
    path("mypage/", Mypage.as_view(), name="mypage"),
    # url(r"list", RareTechLoveView.as_view(), name="list"),
]
