from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

#userのテーブル用クラス
class UserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    ## getter
    def get_id(self):
        try:
            return self.id
        except:
            return False

    def get_name(self):
        try:
            return self.name
        except:
            return False

    def get_email(self):
        try:
            return self.email
        except:
            return False

    def get_password(self):
        try:
            return self.password
        except:
            return False

    def get_is_staff(self):
        try:
            return self.is_staff
        except:
            return False

    ## setter
    def set_name(self, name):
        if name is not None:
            self.name = name
            self.save()

    def set_email(self, email):
        if email is not None:
            self.email = email
            self.save()

    def set_is_staff(self, is_staff):
        if is_staff is not None:
            self.is_staff = is_staff
            self.save()

    def delete(self):
        self.valid = False
        self.save()

#スレッドを取得して保存するためのクラス
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    articlecd = models.IntegerField(verbose_name='記事番号')
    body = models.TextField( verbose_name='質問本文', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Articles')
    ts = models.CharField(max_length=500, unique=True)
    qadist = models.BooleanField(verbose_name='質問フラグ',default=False)

    __Comments = None
    __user_name = None
    __user_icon_path = None

    ## getter
    def get_id(self):
        try:
            return self.id
        except:
            return False

    def get_body(self):
        try:
            return self.body
        except:
            return False

    def get_user(self):
        try:
            return self.user
        except:
            return False

    def get_ts(self):
        try:
            return self.ts
        except:
            return False

    def get_qadist(self):
        try:
            return self.qadist
        except:
            return False

    def get_user_name(self):
        try:
            if self.__user_name is None:
                User = self.get_user()
                if User:
                    self.__user_name = User.get_name()
                else:
                    return False
            return self.__user_name
        except:
            return False

    ## setter
    def set_article_cd(self, articlecd):
        if articlecd is not None:
            self.tarticlecditle = articlecd
            self.save()

    def set_body(self, body):
        if body is not None:
            self.body = body
            self.save()

    def set_user(self, User):
        if User is not None:
            self.user = User
            self.save()

    def delete(self):
        self.valid = False
        self.save()


