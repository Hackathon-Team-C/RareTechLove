# Skip to content
# Why GitHub?
# Team
# Enterprise
# Explore
# Marketplace
# Pricing
# Search
# Sign in
# Sign up
# shiny-a
# /
# RareStudy
# Public
# 13
# Code
# Issues
# Pull requests
# Actions
# Projects
# Wiki
# Security
# Insights
# RareStudy/rarestudy/forms.py /
# @Reimei1213
# Reimei1213 コメント実装
# Latest commit 5a024af on 19 Jun
#  History
#  1 contributor
# 59 lines (44 sloc)  1.6 KB

# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import get_user_model
# from django import forms

# from rarestudy.models.article import Article
# from rarestudy.models.comment import Comment

# User = get_user_model()


# class UserCreateForm(UserCreationForm):

#     class Meta:
#         model = User
#         if User.USERNAME_FIELD == 'email':
#             fields = ('email',)
#         else:
#             fields = ('username', 'email')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'

# class AddArticleForm(forms.ModelForm):

#     class Meta:
#         model = Article
#         fields = ('title', 'body')
#         widgets = {
#             'title' : forms.TextInput(attrs={'placeholder': 'タイトル'})
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'

# class EditUserForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = ('name')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'

# class AddCommentForm(forms.ModelForm):

#     class Meta:
#         model = Comment
#         fields = ('body',)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'
