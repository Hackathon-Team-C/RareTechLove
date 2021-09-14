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
    return False

def import_slack():
  CONVERSATION_URL = 'https://slack.com/api/conversations.history'
  REPLY＿URL = 'https://slack.com/api/conversations.replies'
  TOKEN = os.environ.get("TOKEN")
  CHANNEL_ID = os.environ.get("CHANNEL_ID")
  headers = {"Authorization": "Bearer " + TOKEN}
  params = {
  'channel' : CHANNEL_ID,
  }
  res = requests.get(CONVERSATION_URL, headers=headers, params=params)
  #データをJSONに変換
  json_data = res.json()

  items = json_data['messages']

  tss = []

  count = QuestionTBL.objects.all().count()

  if count > 0 :
    latast_record = QuestionTBL.objects.all().count()
  else:
    latast_record = 0

  for item in items:
    if 'client_msg_id' in item:
        if latast_record == 0 :
          tss.append(item)
        else :
          if QuestionTBL.objects.filter(ts=item['ts']):
            continue
          else:
            tss.append(item)
  for timestamp in tss:
    TS = timestamp['ts']
    params = {
        'channel' : CHANNEL_ID,
        'ts' : TS,
    }
    res = requests.get(REPLY＿URL, headers=headers, params=params)
    json_data = res.json()
    items2 = json_data['messages']
    firstLoop = True
    latast_record = latast_record+1
    ac=None
    for item2 in items2:
          thread_ts = None
          url = None
          match = re.search("(?<=【)*[0-9０-９]+?(?=】)",item2['text'])
          item2['qa_dist']=False
          # タイムスタンプID
          if firstLoop:
            if match :
              item2['qa_dist']= True
              item2['postnumber'] = int(match.group())
              item2['text'] = re.sub('(?<=【)*[0-9０-９]+?(?=】)', '', item2['text'])
              item2['text'] = re.sub('【記事番号】', '', item2['text'])
              # 記事番号(スプレッドシートマスタから取得)
              ac=item2['postnumber']
              qa = item2['qa_dist']
              qt = item2['text']
              try:
                b = UserMST.objects.get(user_name=item2['user'])
              except UserMST.DoesNotExist:
                firstLoop = False
                continue
              uc = b.id
              tsdesu = item2['ts']
              firstLoop = False
            else :
              continue
          qa = item2['qa_dist']
          qt = item2['text']
          try:
            b = UserMST.objects.get(user_name=item2['user'])
          except UserMST.DoesNotExist:
            continue
          uc = b.id
          tsdesu = item2['ts']
          ts_cd= latast_record
          article_cd =ArticleMST.objects.get(id=ac)
          user_cd=UserMST.objects.get(id=uc)
          QuestionTBL.objects.filter().create(qa_dist=qa,ts=tsdesu,question_thread=qt,user_cd=user_cd,article_cd=article_cd,ts_cd=ts_cd)

