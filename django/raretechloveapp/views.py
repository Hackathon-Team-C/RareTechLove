from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .forms import CreateUser
from raretechloveapp.modules import slack
from .models import UserMST
from .models import QuestionTBL
from .models import ArticleMST
# module_dir = os.path.dirname(__file__) # views.pyのあるディレクトリを取得
# json_path = os.path.join(module_dir, 'jojo.json')

# f = open(json_path, 'r')

class raretechlovesignup(TemplateView):
    def post(self, request):
        #form = CreateUser(request.POST, instance=database)
        # form.save()
        form = CreateUser(request.POST)
        username = request.POST.get('user_name')
        password = request.POST.get('pw')
        slack_name = slack.get_user_name(username)
        spread_url = 'https://example.com'

        if UserMST.objects.get(user_name=username):
            form.add_error(None, '残念ながらあなたのSlackIDは何者かによって登録されていますので登録できません、人生早い者勝ちなのです。')
            return render(request, 'raretechloveapp/signup.html', {'form': form})

        UserMST.objects.create(user_name=username,pw=password,slack_name=slack_name,spread_url=spread_url)
        user = User.objects.create_user(username,'',password)

        if user is not None:
            return redirect('login')
        else:
            form.add_error(None, 'そんなslackIDなんて存在しませんよ！！')
            return render(request, 'raretechloveapp/signup.html', {'form': form})

    def get(self, request):
        form = CreateUser()
        return render(request, 'raretechloveapp/signup.html', {'form': form})

class top(LoginRequiredMixin,TemplateView):
    def __init__(self):
        self.params = {}
    def get(self, request, *args, **kwargs):
        self.params["news"] = slack.get_channel_histry(5,0)
        u = UserMST.objects.get(user_name=request.user)
        self.params['my_slack_name'] =u.slack_name
        return render(request, "raretechloveapp/index.html",self.params)
    def post(self, request, *args, **kwargs):
        u = UserMST.objects.get(user_name=request.user)
        self.params['my_slack_name'] =u.slack_name
        return render(request, "raretechloveapp/index.html", self.params)


class raretechlovelogin(TemplateView):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if request.user.is_anonymous:
            return render(request, 'raretechloveapp/login.html',  {'form': form})
        else :
            return redirect('/')

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user.is_anonymous:
             login(request, user)
             return redirect('/')
        else :
            form.add_error(None, 'パスワードをお忘れになりましたか？残念ながら一度忘れたIDは戻ってきません、現実は厳しいのです、あきらめましょう')
            return render(request, 'raretechloveapp/login.html',  {'form': form})

class raretechlovelogout(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class raretechlovepost(LoginRequiredMixin,TemplateView):
    def __init__(self):
        self.params = {}
    def get(self, request, *args, **kwargs):
        self.params["obj"] = slack.get_reply(self.request.GET.get("ts_cd"))
        u = UserMST.objects.get(user_name=request.user)
        self.params['my_slack_name'] =u.slack_name
        return render(request, "raretechloveapp/post.html",self.params)
    def post(self, request, *args, **kwargs):
        self.params["obj"] = slack.get_reply(self.request.GET.get("ts_cd"))
        u = UserMST.objects.get(user_name=request.user)
        self.params['my_slack_name'] =u.slack_name
        return render(request, "raretechloveapp/post.html",self.params)


class raretechlovesearch(LoginRequiredMixin,ListView):
    model = QuestionTBL
    paginate_by = 10
    template_name = 'raretechloveapp/search.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        u = UserMST.objects.get(user_name=self.request.user)
        context['my_slack_name'] =u.slack_name
        context['count'] = QuestionTBL.objects.filter(article_cd =self.request.GET.get('article_cd')).count()
        return context
    def get_queryset(self,**kwargs):
       queryset = super().get_queryset(**kwargs)

       keyword = self.request.GET.get('article_cd')
       if keyword is not None:
            queryset = queryset.filter(article_cd=keyword,qa_dist=True)

       return queryset

class raretechlovemypage(LoginRequiredMixin,TemplateView):
    def __init__(self):
        self.params = {}
    def get(self, request, *args, **kwargs):
        if self.request.GET.get("uname") :
            u = UserMST.objects.get(id=self.request.GET.get("uname"))
            u1 = UserMST.objects.get(user_name=request.user)
            self.params['my_slack_name'] =u1.slack_name
            self.params['slack'] = u.slack_name
        else:
            u = UserMST.objects.get(user_name=request.user)
            self.params['my_slack_name'] =u.slack_name
            self.params['slack'] = u.slack_name
        self.params["news"] = slack.get_channel_histry(10,0,u.id,1)
        self.params["news2"] = slack.get_channel_histry(10,0,u.id,2)
        self.params['question_count'] =slack.question_count(u.id)
        self.params['answer_count'] =slack.answer_count(u.id)
        return render(request, 'raretechloveapp/mypage.html',self.params)
    def post(self, request, *args, **kwargs):
        u = UserMST.objects.get(user_name=request.user)
        self.params['my_slack_name'] =u.slack_name
        return render(request, 'raretechloveapp/mypage.html',self.params)


