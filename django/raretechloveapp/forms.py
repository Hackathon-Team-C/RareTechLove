from .models import UserMST
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CreateUser(forms.ModelForm):
    class Meta():
        model = UserMST  # モデルのインスタンスを生成
        # fields = '__all__'
        pw = forms.CharField(widget=forms.PasswordInput)
        fields = ('user_name', 'pw')
        labels = {
            'user_name': 'SlackID',
            'pw': 'パスワード',
        }
        widgets = {
            'pw': forms.PasswordInput()
        }


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
