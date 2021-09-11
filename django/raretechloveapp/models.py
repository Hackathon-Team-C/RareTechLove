from django.db import models


# 利用者マスタ
class UserMST(models.Model):

    # slackユーザーID
    user_name = models.CharField(max_length=255)
    # raretechloveアプリのパスワード
    pw = models.CharField(max_length=255)
    # Slackの表示名
    slack_name = models.CharField(max_length=255)
    # 300本ノックのスプレッドシートのURL
    spread_url = models.URLField()

    # タイトルにSlackの表示名を表示する
    def __str__(self):
        return self.slack_name


    ## getter
    def get_user_name(self):
        try:
            return self.user_name
        except:
            return False

    def get_pw(self):
        try:
            return self.pw
        except:
            return False

    def get_slack_name(self):
        try:
            return self.slack_name
        except:
            return False

    def get_spread_url(self):
        try:
            return self.spread_url
        except:
            return False


    ## setter
    def set_user_name(self, user_name):
        if user_name is not None:
            self.user_name = user_name
            self.save()

    def set_pw(self, pw):
        if pw is not None:
            self.pw = pw
            self.save()

    def set_slack_name(self, slack_name):
        if slack_name is not None:
            self.slack_name = slack_name
            self.save()

    def set_spread_url(self, spread_url):
        if spread_url is not None:
            self.spread_url = spread_url
            self.save()



# スプレッドシートマスタ
class ArticleMST(models.Model):

    # カテゴリの選択肢
    CATEGORY_CHOICES = (
        ('PC操作', 'PC操作'),
        ('Network', 'Network'),
        ('Web', 'Web'),
        ('Linux', 'Linux'),
        ('プログラミング', 'プログラミング'),
    )

    # 難易度の選択肢
    LEVEL_CHOICES = (
        ('初級', '初級'),
        ('中級', '中級'),
        ('上級', '上級'),
    )

    # 記事リンク先URL
    article_url = models.URLField()
    # スプレッドシートでの記事のカテゴリ
    category = models.CharField(max_length=255, verbose_name="カテゴリ", choices=CATEGORY_CHOICES)
    # 記事の難易度
    level = models.CharField(max_length=255, verbose_name="難易度", choices=LEVEL_CHOICES)

    # タイトルに記事リンク先URLを表示する
    def __str__(self):
        return self.article_url


    ## getter
    def get_article_url(self):
        try:
            return self.article_url
        except:
            return False

    def get_category(self):
        try:
            return self.category
        except:
            return False

    def get_level(self):
        try:
            return self.level
        except:
            return False


    ## setter
    def set_article_url(self, article_url):
        if article_url is not None:
            self.article_url = article_url
            self.save()

    def set_category(self, category):
        if category is not None:
            self.category = category
            self.save()

    def set_level(self, level):
        if level is not None:
            self.level = level
            self.save()



# 難易度テーブル
class DifficultyTBL(models.Model):

    # 記事番号(スプレッドシートマスタから取得)
    article_cd = models.ForeignKey(ArticleMST, on_delete=models.CASCADE)
    # 記事ごとの合計点数(1周目)
    total1 = models.IntegerField()
    # 記事ごとの回答数(1周目)
    answer1 = models.IntegerField()
    # １周目の平均(小数点第2位まで)
    ave1 = models.DecimalField(max_digits=5, decimal_places=2)
    # 記事ごとの合計点数(2周目)
    total2 = models.IntegerField()
    # 記事ごとの回答数(2周目)
    answer2 = models.IntegerField()
    # ２周目の平均(小数点第2位まで)
    ave2 = models.DecimalField(max_digits=5, decimal_places=2)

    # タイトルに記事番号を表示する
    def __str__(self):
        return self.article_cd


    ## getter
    def get_article_cd(self):
        try:
            return self.article_cd
        except:
            return False

    def get_total1(self):
        try:
            return self.total1
        except:
            return False

    def get_answer1(self):
        try:
            return self.answer1
        except:
            return False

    def get_ave1(self):
        try:
            return self.ave1
        except:
            return False

    def get_total2(self):
        try:
            return self.total2
        except:
            return False

    def get_answer2(self):
        try:
            return self.answer2
        except:
            return False

    def get_ave2(self):
        try:
            return self.ave2
        except:
            return False


    ## setter
    def set_article_cd(self, article_cd):
        if article_cd is not None:
            self.article_cd = article_cd
            self.save()

    def set_total1(self, total1):
        if total1 is not None:
            self.total1 = total1
            self.save()

    def set_answer1(self, answer1):
        if answer1 is not None:
            self.answer1 = answer1
            self.save()

    def set_ave1(self, ave1):
        if ave1 is not None:
            self.ave1 = ave1
            self.save()

    def set_total2(self, total2):
        if total2 is not None:
            self.total2 = total2
            self.save()

    def set_answer2(self, answer2):
        if answer2 is not None:
            self.answer2 = answer2
            self.save()

    def set_ave2(self, ave2):
        if ave2 is not None:
            self.ave2 = ave2
            self.save()



# 質問等回数テーブル
class QcountTBL(models.Model):

    # slackユーザーID(利用者マスタから取得)
    user_cd = models.ForeignKey(UserMST, on_delete=models.CASCADE)
    # Slackの質問回数
    question_count = models.IntegerField()
    # Slackの回答回数
    answer_count = models.IntegerField()

    # タイトルにslackユーザーIDを表示する
    def __str__(self):
        return self.user_cd


    ## getter
    def get_user_cd(self):
        try:
            return self.user_cd
        except:
            return False

    def get_question_count(self):
        try:
            return self.question_count
        except:
            return False

    def get_answer_count(self):
        try:
            return self.answer_count
        except:
            return False


    ## setter
    def set_user_cd(self, user_cd):
        if user_cd is not None:
            self.user_cd = user_cd
            self.save()

    def set_question_count(self, question_count):
        if question_count is not None:
            self.question_count = question_count
            self.save()

    def set_answer_count(self, answer_count):
        if answer_count is not None:
            self.answer_count = answer_count
            self.save()



# 質問回答テーブル
class QuestionTBL(models.Model):

    # タイムスタンプID
    ts_cd = models.DateTimeField(null=True, blank=True)
    # 記事番号(スプレッドシートマスタから取得)
    article_cd = models.ForeignKey(ArticleMST, on_delete=models.PROTECT)
    # Slackの質問者・回答者(利用者マスタから取得)
    user_cd = models.ForeignKey(UserMST, on_delete=models.PROTECT)
    # Slackの質問内容
    question_thread = models.TextField()
    # Slackの投稿日時
    ts = models.DateTimeField()
    # 質問者(1)・回答者(0)
    qa_dist = models.BooleanField()

    # タイトルにSlackの質問者・回答者を表示する
    def __str__(self):
        return self.user_cd


    ## getter
    def get_ts_cd(self):
        try:
            return self.ts_cd
        except:
            return False

    def get_article_cd(self):
        try:
            return self.article_cd
        except:
            return False

    def get_user_cd(self):
        try:
            return self.user_cd
        except:
            return False

    def get_question_thread(self):
        try:
            return self.question_thread
        except:
            return False

    def get_ts(self):
        try:
            return self.ts
        except:
            return False

    def get_qa_dist(self):
        try:
            return self.qa_dist
        except:
            return False


    ## setter
    def set_ts_cd(self, ts_cd):
        if ts_cd is not None:
            self.ts_cd = ts_cd
            self.save()

    def set_article_cd(self, article_cd):
        if article_cd is not None:
            self.article_cd = article_cd
            self.save()

    def set_user_cd(self, user_cd):
        if user_cd is not None:
            self.user_cd = user_cd
            self.save()

    def set_question_thread(self, question_thread):
        if question_thread is not None:
            self.question_thread = question_thread
            self.save()

    def set_ts(self, ts):
        if ts is not None:
            self.ts = ts
            self.save()

    def set_qa_dist(self, qa_dist):
        if qa_dist is not None:
            self.qa_dist = qa_dist
            self.save()
