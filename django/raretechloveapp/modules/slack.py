import os
import requests
import re

#test
def test():
  return 'test'


#channelのtsを取得
def get_channel_histry(limit,post_id):
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
  l = {
    'channel' : CHANNEL_ID
  }
  #リクエスト
  res = requests.get(CONVERSATION_URL, headers=headers, params=l)

  #データをJSONに変換
  json_data = res
  json_data = res.json()

  #出力
  items = json_data['messages']
  ts = []
  cnt = 0
  for item in items:
    if 'client_msg_id' in item and cnt < limit:
        item['name'] = get_user_name(item['user'])
        if 'client_msg_id' in item:
            match = re.search("(?<=【)*[0-9０-９]+?(?=】)",item['text'])
            if match :
                item['postnumber'] = match.group()
                if item['postnumber'] == post_id :
                    item['text'] = re.sub('(?<=【)*[0-9０-９]+?(?=】)', '', item['text'])
                    item['text'] = re.sub('【記事番号】', '', item['text'])
                    ts.append(item)
                elif post_id == 0 :
                    item['text'] = re.sub('(?<=【)*[0-9０-９]+?(?=】)', '', item['text'])
                    item['text'] = re.sub('【記事番号】', '', item['text'])
                    ts.append(item)
    cnt+=1
  return ts

def get_reply(ts):
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
      params = {
          'channel' : CHANNEL_ID,
          'ts' : ts,
      }
      res = requests.get(REPLY＿URL, headers=headers,params=params)
      json_data = res.json()
      items = json_data['messages']
      result = []
      for item in items:
          item['name'] = get_user_name(item['user'])
          match = re.search("(?<=【)*[0-9０-９]+?(?=】)",item['text'])
          if match :
            item['postnumber'] = match.group()
          item['text'] = re.sub('(?<=【)*[0-9０-９]+?(?=】)', '', item['text'])
          item['text'] = re.sub('【記事番号】', '', item['text'])
          result.append(item)
      return result

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
