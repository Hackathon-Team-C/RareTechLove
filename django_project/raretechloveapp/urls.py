from django.conf.urls import url
from .views import raretechloveappView
#from .views import raretechloveappSearchView

urlpatterns = [
    url(r"", raretechloveappView.as_view(), name="index"),
    url(r"/login", raretechloveappView.as_view(), name="login"),
    url(r"/signup", raretechloveappView.as_view(), name="signup"),
]
