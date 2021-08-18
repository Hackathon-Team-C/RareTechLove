from django.contrib import admin
from django.urls import path
from .views import topview, signupview, loginview, logoutview

urlpatterns = [
    path('', topview, name='top'),
    path('signup/', signupview, name='signup'),
    path('login/', loginview, name='login'),
    path('logout/', logoutview, name='logout'),
]