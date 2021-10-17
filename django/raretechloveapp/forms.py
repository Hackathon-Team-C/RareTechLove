from .models import UserMST
from django import forms
from django.contrib.auth.forms import AuthenticationForm

# 新規ユーザーを登録するためのフォーム　forms.ModelFormとかくとデーターベースのモデルを指定できる
class CreateUser(forms.ModelForm):
    class Meta():
        model = UserMST  # モデルのインスタンスを生成
        # allとするとモデルのフィールドを全部取得して表示する
        # fields = '__all__'
        pw = forms.CharField(widget=forms.PasswordInput)
        fields = ('user_name', 'pw')
        labels = {
            'user_name': 'SlackID',
            'pw': 'パスワード',
        }
        # パスワードにするためのおまじない
        widgets = {
            'pw': forms.PasswordInput()
        }

# ログインするときに使われるフォーム
class LoginForm(AuthenticationForm):
    # 引数はまぁ・・・理解しなくても良さそうだし、なんかうんそういうものだと思って！
    def __init__(self, *args, **kwargs):
        # 親クラスを継承しますって記述　親クラスはAuthenticationForm認証用のフォーム
        super().__init__(*args, **kwargs)
        # フィールドのシーケンスを返すそうです。と言われてもわからないと思うのですが簡単に言うとここでは認証用フォームにあるログインIDとパスワードのことを指すのだなあと思っておいてください
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
