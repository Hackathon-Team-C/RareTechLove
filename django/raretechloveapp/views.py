from django.shortcuts import render, redirect
# redirect 特徴：templates(html)に何も渡さない。 単に対象のURLに遷移したいときに使用する。 return redirect('https://example.com/')
# render 特徴：redirectとの違いはtemplates(html)に変数等を渡せる。
#     return render(request, 'myapp/index.html', {
#        'foo': 'bar',})　#第三引数に辞書型で渡す値を指定する
from django.views.generic import TemplateView
# Djangoには目的に沿った画面を構築するためのクラスがいくつか用意されています。Djangoにおいてこれらのクラスは、ジェネリックビューや汎用ビュー(Generic views)などと呼ばれています。その基本となるクラスの一つがTemplateViewです。
# 簡単にテンプレートファイルやモデルと連携できるメリットがあります。View関数と比較して少ないコードで多様な機能を実装できるのが特徴です。
#get_context_data関数でテンプレートに変数の受け渡しを、post関数やget関数などあります。
# ListView　一覧画面
# CreateView　新規作成画面
# UpdateView　編集画面
# DetailView　詳細画面
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# viewsでログインユーザのみの実行を許可をするためのクラス
from django.contrib.auth.models import User
#djangoの元々のユーザークラスをインポート
from django.contrib.auth import authenticate, login, logout
# authenticate
# ユーザ名とパスワードで認証します。
# login
# 認証されたユーザを使ってログインします。
# logout
# ログアウトします。
from .forms import LoginForm
# formsで書いた処理をとってくる
from .forms import CreateUser
# formsで書いた処理をとってくる
from raretechloveapp.modules import slack
# modulesから特定のモジュールを取ってくる。
from .models import UserMST
# modelsのクラスをとってくる（db）
#modelから特定のクラスを持ってくる
from .models import QuestionTBL
# modelsのクラスをとってくる（db）
#modelから特定のクラスを持ってくる
from .models import ArticleMST
# modelsのクラスをとってくる（db）

# 新規登録
class raretechlovesignup(TemplateView):
    def post(self, request):
        #forms.pyのクラスに引数は、ログイン情報のデータを受け渡す
        form = CreateUser(request.POST)
        username = request.POST.get('user_name')
        password = request.POST.get('pw')
        # modulesのslack.pyの関数を取得 slackに名前が存在しているかチェック
        slack_name = slack.get_user_name(username)
        # 果たしてこれはもうこれはいらないのではなかろうか
        spread_url = 'https://example.com'

        # slackにそんな名前はなかったよというときのエラーハンドリング
        if slack_name == False:
            form.add_error(None, 'そのようなSlackIDは見たことがありません！是非ともお見せしていただきたいですね')
            return render(request, 'raretechloveapp/signup.html', {'form': form})

        try:
            # 同じユーザーが登録されていたら
            if UserMST.objects.all().count() != 0 and UserMST.objects.get(user_name=username):
                form.add_error(None, '残念ながらあなたのSlackIDは何者かによって登録されていますので登録できません、人生早い者勝ちなのです。')
                return render(request, 'raretechloveapp/signup.html', {'form': form})
        except UserMST.DoesNotExist:
                    #データーベースにユーザー情報を登録させる
                    UserMST.objects.create(user_name=username,pw=password,slack_name=slack_name,spread_url=spread_url)
                    #Djangoに新規登録する、ユーザーID、email、password
                    user = User.objects.create_user(username,'',password)

                    #djangoのデーターベースにユーザーが存在すればログイン
                    if user is not None:
                        login(request, user)
                        return redirect('/')
                    else:
                        #ユーザーが存在しなければ怒られる
                        form.add_error(None, 'そんなslackIDなんて存在しませんよ！！')
                        return render(request, 'raretechloveapp/signup.html', {'form': form})
        #エラーハンドリングの時の通常処理
        UserMST.objects.create(user_name=username,pw=password,slack_name=slack_name,spread_url=spread_url)
        user = User.objects.create_user(username,'',password)

        if user is not None:
            login(request, user)
            slack.import_slack()
            return redirect('/')
        else:
            form.add_error(None, 'そんなslackIDなんて存在しませんよ！！')
            return render(request, 'raretechloveapp/signup.html', {'form': form})

    def get(self, request):
        #forms.pyからformの情報を引っ張ってくる
        form = CreateUser()
        return render(request, 'raretechloveapp/signup.html', {'form': form})

# トップページ
class top(LoginRequiredMixin,TemplateView):
    def __init__(self):
        #変数の枠を作るのだ
        self.params = {}
    def get(self, request, *args, **kwargs):
        #テンプレートに受け渡す変数名を指定する、ここではnewsの中にslackの関数から取得した新着情報５件を値として格納する
        self.params["news"] = slack.get_channel_histry(5,0)
        #dbの情報をuser_nameと一致するログインIDから情報を取ってくる
        u = UserMST.objects.get(user_name=request.user)
        # slack_nameをDBから取得
        self.params['my_slack_name'] =u.slack_name
        # 全ユーザー情報が入ったDBを丸ごと取得
        self.params['all_user'] = UserMST.objects.all()
        return render(request, "raretechloveapp/index.html",self.params)
    # post関数使わない定義だけ
    def post(self, request, *args, **kwargs):
        u = UserMST.objects.get(user_name=request.user)
        # slack_nameをDBから取得
        self.params['my_slack_name'] =u.slack_name
        # 全ユーザー情報が入ったDBを丸ごと取得
        self.params['all_user'] = UserMST.objects.all()
        return render(request, "raretechloveapp/index.html", self.params)

# ログインページ
class raretechlovelogin(TemplateView):
    def get(self, request, *args, **kwargs):
        # forms.pyのログインフォームを取得
        form = LoginForm(request.POST or None)
        # ユーザーがログインしてない状態かどうかで分岐
        if request.user.is_anonymous:
            return render(request, 'raretechloveapp/login.html',  {'form': form})
        else :
            return redirect('/')

    def post(self, request, *args, **kwargs):
        # forms.pyのログインフォームを取得
        form = LoginForm(request.POST or None)
        username = request.POST.get('username')
        password = request.POST.get('password')
        # djangoでログイン認証するための記述
        user = authenticate(request, username=username, password=password)
        # 認証に成功していたらログイン
        if user.is_anonymous:
             login(request, user)
             return redirect('/')
        else :
            form.add_error(None, 'パスワードをお忘れになりましたか？残念ながら一度忘れたIDは戻ってきません、現実は厳しいのです、あきらめましょう')
            return render(request, 'raretechloveapp/login.html',  {'form': form})

# ログアウト画面　難しそうじゃないと思うのでコメント入れてませんw
class raretechlovelogout(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    # post関数使わない定義だけ
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
# スレッドページ
class raretechlovepost(LoginRequiredMixin,TemplateView):
    def __init__(self):
        # 変数の枠を作る
        self.params = {}
    def get(self, request, *args, **kwargs):
        # 変数objにスレッド返信含むを取得
        self.params["obj"] = slack.get_reply(self.request.GET.get("ts_cd"))
        # 現在のログインしているユーザーのDBのオブジェクトを取得
        u = UserMST.objects.get(user_name=request.user)
        # 全てのUserMSTのオブジェクト取得
        self.params['all_user'] = UserMST.objects.all()
        # slack＿nameを取得
        self.params['my_slack_name'] =u.slack_name
        return render(request, "raretechloveapp/post.html",self.params)
    # post関数使わない定義だけ
    def post(self, request, *args, **kwargs):
       # 変数objにスレッド返信含むを取得
        self.params["obj"] = slack.get_reply(self.request.GET.get("ts_cd"))
        u = UserMST.objects.get(user_name=request.user)
        self.params['all_user'] = UserMST.objects.all()
        self.params['my_slack_name'] =u.slack_name
        return render(request, "raretechloveapp/post.html",self.params)

# 検索結果
class raretechlovesearch(LoginRequiredMixin,ListView):
    # モデルのクラスを指定
    model = QuestionTBL
    # 表示件数を指定
    paginate_by = 5
    template_name = 'raretechloveapp/search.html'
    # どのような変数をテンプレートに渡すか指定
    def get_context_data(self, **kwargs):
        # self.paramsみたいなもの
        context = super().get_context_data(**kwargs)
        # 現在ログイン中のユーザー情報をデーターベースから取得
        u = UserMST.objects.get(user_name=self.request.user)
        # 現在ログイン中のslack_nameを取得
        context['my_slack_name'] =u.slack_name
        # 検索した記事番号を取得
        keyword = self.request.GET.get('article_cd')
        # 記事番号が無ければ
        if keyword is not None:
            # count変数に全ての記事のカウントを取得
            context['count'] = QuestionTBL.objects.filter(article_cd =self.request.GET.get('article_cd')).count()
        # UserMSTの全オブジェクト取得
        context['all_user'] = UserMST.objects.all()
        # 検索してきたユーザー番号取得
        context['user_cd'] =self.request.GET.get('user_cd')
        # 検索してきた記事番号取得
        context['article_cd'] =self.request.GET.get('article_cd')
        # ユーザー番号が取得できた時
        if context['user_cd'] is not None:
            # ユーザー絞り込みしたオブジェクトを取得
            context['user_slack_name'] =UserMST.objects.get(id=context['user_cd'])
        return context
    # query検索結果をどうやって表示するか
    def get_queryset(self,**kwargs):
       # クエリーを取得
       queryset = super().get_queryset(**kwargs)
       # 検索してきた記事番号を取得
       keyword = self.request.GET.get('article_cd')
       # 検索してきたユーザー番号を取得
       keyword2 = self.request.GET.get('user_cd')

       # 記事番号取得していたら
       if keyword is not None:
            # ユーザー番号を取得できていたら
            if keyword2 is not None:
                queryset = queryset.filter(article_cd=keyword,user_cd=keyword2,qa_dist=True)
            # ユーザー番号を取得できていなかったら
            else:
                queryset = queryset.filter(article_cd=keyword,qa_dist=True)
       # 記事番号取得できなかったら
       else :
            # ユーザー番号を取得できていたら
            if keyword2 is not None:
                queryset = queryset.filter(user_cd=keyword2,qa_dist=True)
            # ユーザー番号を取得できなかったら
            else:
                queryset = queryset.filter(qa_dist=True)

       return queryset

# マイページの処理
class raretechlovemypage(LoginRequiredMixin,TemplateView):
    def __init__(self):
        # 変数を定義するための枠
        self.params = {}
    def get(self, request, *args, **kwargs):
        #ユーザーネームを取得できていたら 自分以外のマイページ
        if self.request.GET.get("uname") :
            u = UserMST.objects.get(id=self.request.GET.get("uname"))
            u1 = UserMST.objects.get(user_name=request.user)
            self.params['my_slack_name'] =u1.slack_name
            self.params['slack'] = u.slack_name
        #ログイン中のユーザーだったら
        else:
            u = UserMST.objects.get(user_name=request.user)
            self.params['my_slack_name'] =u.slack_name
            self.params['slack'] = u.slack_name
        self.params["news"] = slack.get_channel_histry(10,0,u.id,1)
        self.params["news2"] = slack.get_channel_histry(10,0,u.id,2)
        #ユーザーの質問数カウント
        self.params['question_count'] =slack.question_count(u.id)
        #ユーザーの回答数カウント
        self.params['answer_count'] =slack.answer_count(u.id)
        self.params['all_user'] = UserMST.objects.all()
        return render(request, 'raretechloveapp/mypage.html',self.params)
    # post関数使わないけど定義だけ
    def post(self, request, *args, **kwargs):
        u = UserMST.objects.get(user_name=request.user)
        self.params['my_slack_name'] =u.slack_name
        self.params['all_user'] = UserMST.objects.all()
        return render(request, 'raretechloveapp/mypage.html',self.params)


