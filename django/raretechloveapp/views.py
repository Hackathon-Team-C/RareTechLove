from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.db import IntegrityError
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
#from .forms import UserCreateForm
from .forms import LoginForm
from .forms import CreateUser
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

class signup(TemplateView):
    def post(self, request):
        database = UserMST()
        form = CreateUser(request.POST, instance=database)
        form.save()
        user_name = request.POST.get('user_name')
        pw = request.POST.get('pw')
        user = User.objects.create_user(user_name,'',pw)
        if user is not None:
            #ログイン
            login(request, user)
            return render(request, 'raretechloveapp/index.html', {'form': form})
        else:
            return render(request, 'raretechloveapp/signup.html', {'form': form})
        login(request, user)
        return render(request, 'raretechloveapp/index.html', {'form': form})

    def get(self, request):
        form = CreateUser()
        return render(request, 'raretechloveapp/signup.html', {'form': form})

class top(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'raretechloveapp/index.html', {})
    def post(self, request, *args, **kwargs):
        return render(request, 'raretechloveapp/index.html', {})


class login(TemplateView):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        user_name = request.POST.get('user_name')
        pw = request.POST.get('pw')
        user = authenticate(request, username=user_name, password=pw)
        return render(request, 'raretechloveapp/login.html',  {'form': form})
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        return render(request, 'raretechloveapp/login.html',  {'form': form})

class logout(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'raretechloveapp/login.html', {})
    def post(self, request, *args, **kwargs):
        logout(request)
        return render(request, 'raretechloveapp/login.html', {})

class mypage(TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'raretechloveapp/index.html', {})
    def post(self, request, *args, **kwargs):
        return render(request, 'raretechloveapp/index.html', {})

