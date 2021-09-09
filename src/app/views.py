from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.views.generic import TemplateView
#from django.views.generic import ListView
#from .models import Article
import json
import requests
import re
import os

class raretechloveappView(TemplateView):
        def __init__(self):
        #   self.CONVERSATION_URL = 'https://slack.com/api/conversations.history'
        #   #conversations.replies
        #   self.REPLY＿URL = 'https://slack.com/api/conversations.replies'
        #   #appトークン
        #   self.TOKEN = os.environ.get("TOKEN")
        #   #ハッカソンチャンネルID
        #   self.CHANNEL_ID = os.environ.get("CHANNEL_ID")
        #   #userlist
        #   self.USER_LIST = 'https://slack.com/api/users.list'
        #   #ヘッダー
        #   self.headers = {"Authorization": "Bearer " + self.TOKEN}
          self.params = {
                "title": "title",
          }

        def all_user_name(self):
            res = requests.get(self.USER_LIST, headers=self.headers)
            json_data = res.json()
            items = json_data['members']
            m = []
            for item in items:
                if item['is_bot'] ==  False:
                    m.append(item)
            return m

        def get_user_name(self,id):
            all = self.all_user_name()
            for item in all:
                if item['id'] == id:
                    return item['real_name']

        #channelのtsを取得
        def get_channel_histry(self,limit,post_id):
             l = {
                'channel' : self.CHANNEL_ID
             }
             #リクエスト
             res = requests.get(self.CONVERSATION_URL, headers=self.headers, params=l)

             #データをJSONに変換
             json_data = res
             json_data = res.json()

             #出力
             items = json_data['messages']
             ts = []
             cnt = 0
             for item in items:
                if 'client_msg_id' in item and cnt < limit:
                    item['name'] = self.get_user_name(item['user'])
                    if 'client_msg_id' in item:
                        match = re.search("(?<=【)*[0-9０-９]+?(?=】)",item['text'])
                        if match :
                            item['postnumber'] = match.group()
                            if item['postnumber'] == post_id :
                                item['text'] = re.sub('(?<=【)*[0-9０-９]+?(?=】)', '', item['text'])
                                item['text'] = re.sub('【記事番号】', '', item['text'])
                                ts.append(item)
                            elif post_id == 0 :
                                item['text'] = re.sub('(?<=【)*[0-9０-９]+?(?=】)', '', item['text'])
                                item['text'] = re.sub('【記事番号】', '', item['text'])
                                ts.append(item)
                cnt+=1
             return ts

        def get_reply(self,ts):
                 #TS = 'C029TH76EP4-1630933007.001100'
                 #TS = ts['ts']
                 params = {
                     'channel' : self.CHANNEL_ID,
                     'ts' : ts,
                 }
                 res = requests.get(self.REPLY＿URL, headers=self.headers,params=params)
                 json_data = res.json()
                 items = json_data['messages']
                 result = []
                 for item in items:
                     item['name'] = self.get_user_name(item['user'])
                     match = re.search("(?<=【)*[0-9０-９]+?(?=】)",item['text'])
                     if match :
                        item['postnumber'] = match.group()
                     item['text'] = re.sub('(?<=【)*[0-9０-９]+?(?=】)', '', item['text'])
                     item['text'] = re.sub('【記事番号】', '', item['text'])
                     result.append(item)
                 return result

        def get(self, request):
            path = request.path
            if path == '/search' :
                self.params["ARTICLE_CD"] = request.GET.get("ARTICLE_CD")
                self.params["obj"] = self.get_channel_histry(5,self.params["ARTICLE_CD"])
                return render(request, "raretechloveapp/search.html", self.params)
            elif path == '/st' :
                self.params["obj"] = self.get_reply(request.GET.get("TS_CD"))
                return render(request, "raretechloveapp/st.html", self.params)
            elif path == '/' :
                #self.params['news'] = self.get_channel_histry(5,0)
                return render(request, "raretechloveapp/index.html", self.params)
            else :
                return render(request, "raretechloveapp/"+ path +".html", self.params)

        def post(self, request):
                #obj = TodoDB()
                #todoform = TodoForm(request.POST, instance=obj)
                #todoform.save()
                return render(request, "/raretechloveapp/index.html", self.params)










# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.db import IntegrityError
# from django.contrib.auth import authenticate, login, logout

# # Create your views here.
# def topview(request):
#     return render(request, 'top.html', {'hello': 'Hello'})

# def signupview(request):
#     if request.method == 'POST':
#         username_data = request.POST.get('username_data')
#         password_data = request.POST.get('password_data')
#         try:
#             user = User.objects.create_user(username_data, '', password_data)
#         except IntegrityError:
#             return render(request, 'signup.html', {'error': 'このユーザーは登録されています'})
#     else:
#         return render(request, 'signup.html', {})
#     return render(request, 'signup.html', {})

# def loginview(request):
#     if request.method == 'POST':
#         username_data = request.POST.get('username_data')
#         password_data = request.POST.get('password_data')
#         user = authenticate(request, username=username_data, password=password_data)
#         if user is not None:
#             login(request, user)
#             return redirect('top_page')
#         else:
#             return redirect('login')
#     return render(request, 'login.html')

# def logoutview(request):
#     logout(request)
#     return redirect('login')
