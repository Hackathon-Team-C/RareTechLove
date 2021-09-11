from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.db import IntegrityError
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreateForm
from django.contrib.auth import (
     get_user_model, logout as auth_logout,
)
from .models import Article
User = get_user_model()
import json
import requests
import re
import os

module_dir = os.path.dirname(__file__) # views.pyのあるディレクトリを取得
json_path = os.path.join(module_dir, 'jojo.json')

f = open(json_path, 'r')

class SignUp(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'raretechloveapp/signup.html'

class Login(LoginView):
    template_name = "raretechloveapp/login.html"

class Logout(LogoutView):
    template_name = "raretechloveapp/logout.html"

class Top(LoginRequiredMixin,TemplateView):
    template_name = 'raretechloveapp/index.html'
    model = Article
    context_object_name = 'Articles'

    def get_queryset(self):
        obj = Article.objects.all()
        return obj

class Mypage(LoginRequiredMixin,TemplateView):
    template_name = 'raretechloveapp/mypage.html'

# class RareTechLoveView(LoginRequiredMixin,TemplateView):
#         def __init__(self):
#           #チャンネルヒストリー
#           self.CONVERSATION_URL = 'https://slack.com/api/conversations.history'
#           #conversations.replies
#           self.REPLY＿URL = 'https://slack.com/api/conversations.replies'
#           #appトークン
#           self.TOKEN = os.environ.get("TOKEN")
#           #ハッカソンチャンネルID
#           self.CHANNEL_ID = os.environ.get("CHANNEL_ID")
#           #userlist
#           self.USER_LIST = 'https://slack.com/api/users.list'
#           #いい感じにslackからメッセージが取れる魔法の呪文
#           self.headers = {"Authorization": "Bearer " + self.TOKEN}
#           self.params ={}

#         def all_user_name(self):
#             res = requests.get(self.USER_LIST, headers=self.headers)
#             json_data = res.json()
#             items = json_data['members']
#             m = []
#             for item in items:
#                 if item['is_bot'] ==  False:
#                     m.append(item)
#             return m

#         def get_user_name(self,id):
#             all = self.all_user_name()
#             for item in all:
#                 if item['id'] == id:
#                     return item['real_name']

#         #channelのtsを取得
#         def get_channel_histry(self,limit,post_id):
#              l = {
#                 'channel' : self.CHANNEL_ID
#              }
#              #リクエスト
#              res = requests.get(self.CONVERSATION_URL, headers=self.headers, params=l)

#              #データをJSONに変換
#              json_data = res
#              json_data = res.json()

#              #出力
#              items = json_data['messages']
#              ts = []
#              cnt = 0
#              for item in items:
#                 if 'client_msg_id' in item and cnt < limit:
#                     item['name'] = self.get_user_name(item['user'])
#                     if 'client_msg_id' in item:
#                         match = re.search("(?<=【)*[0-9０-９]+?(?=】)",item['text'])
#                         if match :
#                             item['postnumber'] = match.group()
#                             if item['postnumber'] == post_id :
#                                 item['text'] = re.sub('(?<=【)*[0-9０-９]+?(?=】)', '', item['text'])
#                                 item['text'] = re.sub('【記事番号】', '', item['text'])
#                                 ts.append(item)
#                             elif post_id == 0 :
#                                 item['text'] = re.sub('(?<=【)*[0-9０-９]+?(?=】)', '', item['text'])
#                                 item['text'] = re.sub('【記事番号】', '', item['text'])
#                                 ts.append(item)
#                 cnt+=1
#              return ts

#         def get_reply(self,ts):
#                  #TS = 'C029TH76EP4-1630933007.001100'
#                  #TS = ts['ts']
#                  params = {
#                      'channel' : self.CHANNEL_ID,
#                      'ts' : ts,
#                  }
#                  res = requests.get(self.REPLY＿URL, headers=self.headers,params=params)
#                  json_data = res.json()
#                  items = json_data['messages']
#                  result = []
#                  for item in items:
#                      item['name'] = self.get_user_name(item['user'])
#                      match = re.search("(?<=【)*[0-9０-９]+?(?=】)",item['text'])
#                      if match :
#                         item['postnumber'] = match.group()
#                      item['text'] = re.sub('(?<=【)*[0-9０-９]+?(?=】)', '', item['text'])
#                      item['text'] = re.sub('【記事番号】', '', item['text'])
#                      result.append(item)
#                  return result

#         # def signupview(request):
#         #     if request.method == 'POST':
#         #         username_data = request.POST.get('username_data')
#         #         password_data = request.POST.get('password_data')
#         #         try:
#         #             user = User.objects.create_user(username_data, '', password_data)
#         #         except IntegrityError:
#         #             return render(request, 'signup.html', {'error': 'このユーザーは登録されています'})
#         #     else:
#         #         return render(request, 'signup.html', {})
#         #     return render(request, 'signup.html', {})

#         #ログインしてなかったら最初にログインページに飛ばすよ
#         #def loginredirect(self,request):
#             #path = request.path
#             #if path != '/login' and path != '/signup':
#                     # username_data = request.POST.get('username_data')
#                     # password_data = request.POST.get('password_data')
#                     # user = authenticate(request, username=username_data, password=password_data)
#                     # if user is not None:
#                     #     login(request, user)
#                     #     return True
#                     # else:
#                     #     return
#                     #ログインしてます ならば該当のページへゴー
#                     #してませんならばログインするが良い！


#         # def logoutview(self,request):
#         #     logout(request)
#         #     return render(request, "raretechloveapp/login.html")

#         def get(self, request):
#             path = request.path
#             if path == '/search' :
#                 self.params["ARTICLE_CD"] = request.GET.get("ARTICLE_CD")
#                 self.params["obj"] = self.get_channel_histry(5,self.params["ARTICLE_CD"])
#                 if self.params["obj"] :
#                     return render(request, "raretechloveapp/search.html", self.params)
#                 else :
#                     self.params["obj"] == -1
#                     return render(request, "raretechloveapp/search.html", self.params)
#             elif path == '/post' :
#                 self.params["obj"] = self.get_reply(request.GET.get("TS_CD"))
#                 return render(request, "raretechloveapp/post.html", self.params)
#             elif path == '/mypage':
#                 self.params["r"] = "mypage"
#                 return render(request, "raretechloveapp/mypage.html", self.params)
#             elif path == '/':
#                 #self.params['news'] = self.get_channel_histry(5,0)
#                 self.params["r"] = "index"
#                 return render(request, "raretechloveapp/index.html", self.params)
#             # else :
#             #     return render(request, "raretechloveapp/"+ path +".html", self.params)

#         def post(self, request):
#                 path = request.path
#                 #obj = TodoDB()
#                 #todoform = TodoForm(request.POST, instance=obj)
#                 #todoform.save()
#                 return render(request, "/raretechloveapp/index.html", self.params)














