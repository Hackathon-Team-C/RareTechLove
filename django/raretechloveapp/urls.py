from django.urls import path
#from .views import Top,Login,SignUp,Mypage,Logout
from .views import signup
from .views import top
from .views import login
from .views import logout
from .views import mypage

urlpatterns = [
    path('', top.as_view(), name='index'),
    path("login/", login.as_view(), name="login"),
    path('logout/',logout.as_view(), name='logout'),
    path("signup/", signup.as_view(), name="signup"),
    path("mypage/", mypage.as_view(), name="mypage"),
    # url(r"list", RareTechLoveView.as_view(), name="list"),
]
