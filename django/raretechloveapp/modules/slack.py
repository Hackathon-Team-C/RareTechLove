import os
import requests
import re
from ..models import QuestionTBL
from ..models import UserMST
from ..models import ArticleMST
#test
def test():
  return 'test'

#ユーザーのスラックに応じてカウント
def question_count(user_cd):
  items = QuestionTBL.objects.filter(user_cd=user_cd,qa_dist=True).count()
  return items

#ユーザーのスラックに応じてカウント
def answer_count(user_cd):
  items = QuestionTBL.objects.filter(user_cd=user_cd,qa_dist=False).count()
  return items


#channelのtsを取得
def get_channel_histry(limit=1000,post_id=0,user_cd=0,qa_dist=1):

  if qa_dist == 2 :
     qa_dist=False
  items = QuestionTBL.objects.filter(qa_dist=qa_dist)
  cnt = 0
  ts=[]
  if user_cd != 0 :
    for item in items:
      if cnt < limit :
        if user_cd == item.user_cd_id :
          if item.article_cd == post_id:
              ts.append(item)
          elif post_id == 0 :
              ts.append(item)
        cnt=1+cnt
    return ts
  else :
    for item in items:
      if cnt < limit :
          if item.article_cd == post_id:
              ts.append(item)
          elif post_id == 0 :
              ts.append(item)
      cnt=1+cnt
  return ts

def get_reply(ts_cd):
      items = QuestionTBL.objects.filter(ts_cd=ts_cd)
      return items

def get_user_name(id):
    CONVERSATION_URL = 'https://slack.com/api/conversations.history'
    #conversations.replies
    REPLY＿URL = 'https://slack.com/api/conversations.replies'
    #appトークン
    TOKEN = os.environ.get("TOKEN")
    #ハッカソンチャンネルID
    CHANNEL_ID = os.environ.get("CHANNEL_ID")
    #userlist
    USER_LIST = 'https://slack.com/api/users.list'
    #ヘッダー
    headers = {"Authorization": "Bearer " + TOKEN}
    res = requests.get(USER_LIST, headers=headers)
    json_data = res.json()
    items = json_data['members']
    result = []
    for item in items:
      if item['is_bot'] ==  False:
        result.append(item)
    all = result
    for item in all:
        if item['id'] == id:
          return item['real_name']
