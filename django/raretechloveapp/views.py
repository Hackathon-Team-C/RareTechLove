from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.db import IntegrityError
from django.views.generic import TemplateView
from django.views.generic import ListView,CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
#from .forms import UserCreateForm
from .forms import LoginForm
from .forms import CreateUser
from raretechloveapp.modules import slack
from django.contrib.auth import (
     get_user_model, logout as auth_logout,
)
from .models import UserMST
from .models import ArticleMST
User = get_user_model()
import json
import requests
import re
import os

# module_dir = os.path.dirname(__file__) # views.pyのあるディレクトリを取得
# json_path = os.path.join(module_dir, 'jojo.json')

# f = open(json_path, 'r')

class raretechlovesignup(TemplateView):
    def post(self, request):
        #form = CreateUser(request.POST, instance=database)
        # form.save()
        username = request.POST.get('user_name')
        password = request.POST.get('pw')
        slack_name = slack.get_user_name(username)
        spread_url = 'https://example.com'
        UserMST.objects.create(user_name=username,pw=password,slack_name=slack_name,spread_url=spread_url)
        user = User.objects.create_user(username,'',password)

        if user is not None:
            return redirect('login')
        else:
            return render(request, 'raretechloveapp/signup.html')

    def get(self, request):
        form = CreateUser()
        return render(request, 'raretechloveapp/signup.html', {'form': form})

class top(LoginRequiredMixin,TemplateView):
    def get(self, request, *args, **kwargs):
        self.params["obj"] = get_reply(request.GET.get("TS_CD"))
        return render(request, 'raretechloveapp/index.html', self.params)
    def post(self, request, *args, **kwargs):
        return render(request, 'raretechloveapp/index.html', {})


class raretechlovelogin(TemplateView):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if request.user.is_anonymous:
            return render(request, 'raretechloveapp/login.html',  {'form': form})
        else :
            return redirect('index')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user.is_anonymous:
             login(request, user)
             return redirect('/')
        else :
            return render(request, 'raretechloveapp/login.html',  {'form': form})

class raretechlovelogout(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class raretechlovemypage(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'raretechloveapp/mypage.html', {})
    def post(self, request, *args, **kwargs):
        return render(request, 'raretechloveapp/mypage.html', {})


