from django.contrib.sites import requests
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def topview(request):
    return render(request, 'top.html', {'hello': 'Hello'})


def signupview(request):
    USER_LIST = 'https://slack.com/api/users.list'
    TOKEN = 'xoxp-2333779462451-2337966012902-2388925887554-1c34b66f22368d2415e5f773806b30d5'
    headers = {"Authorization": "Bearer " + TOKEN}

    if request.method == 'POST':
        res = requests.get(USER_LIST, headers=headers)
        json_data = res.json()
        members = json_data['members']
        member_ID = [member['id'] for member in members if member['is_bot'] == False]
        posted_slack_ID = request.POST.get('slack_ID')
        if posted_slack_ID in member_ID:
            slack_Id = posted_slack_ID
            slack_name = request.POST.get('slack_name')
            password = request.POST.get('password_data')
            User_List.objects.create(slack_Id=slack_Id, real_name=slack_name, password=password)
        else:
            return render(request, 'signup.html', {'error': 'メンバー限定のslackに参加してください'})
    else:

        return render(request, 'signup.html', {})
    return render(request, 'top.html', {})


def loginview(request):
    if request.method == 'POST':
        username_data = request.POST.get('username_data')
        password_data = request.POST.get('password_data')
        user = authenticate(request, username=username_data, password=password_data)
        if user is not None:
            login(request, user)
            return redirect('top_page')
        else: 
            return redirect('login')
    return render(request, 'login.html')

def logoutview(request):
    logout(request)
    return redirect('login')