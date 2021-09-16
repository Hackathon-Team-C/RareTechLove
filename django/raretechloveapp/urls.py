from django.urls import path
# from .views import Top,Login,SignUp,Mypage,Logout
from .views import raretechlovesignup
from .views import top
from .views import raretechlovelogin
from .views import raretechlovelogout
from .views import raretechlovemypage
from .views import raretechlovesearch
from .views import raretechlovepost
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', top.as_view(), name='index'),
    # path('index/', top.as_view(), name='index'),
    path("login/", auth_views.LoginView.as_view(template_name="raretechloveapp/login.html"), name="login"),
    path('logout/', raretechlovelogout.as_view(), name='logout'),
    path("signup/", raretechlovesignup.as_view(), name="signup"),
    path("mypage/", raretechlovemypage.as_view(), name="mypage"),
    path("search/", raretechlovesearch.as_view(), name="search"),
    path("post/", raretechlovepost.as_view(), name="post"),
]
