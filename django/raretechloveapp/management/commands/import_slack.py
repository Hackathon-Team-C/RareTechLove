from django.core.management.base import BaseCommand
from django.db.models.fields import NullBooleanField
import requests
from django.utils import timezone
from ...models import QuestionTBL
from ...models import UserMST
from ...models import ArticleMST
import os
import re


class Command(BaseCommand):
    def handle(self, *args, **options):
        CONVERSATION_URL = 'https://slack.com/api/conversations.history'
        REPLY＿URL = 'https://slack.com/api/conversations.replies'
        TOKEN = os.environ.get("TOKEN")
        CHANNEL_ID = os.environ.get("CHANNEL_ID")
        headers = {"Authorization": "Bearer " + TOKEN}

        def get_channel_histry(self):
            params = {
                'channel': CHANNEL_ID,
            }
            res = requests.get(CONVERSATION_URL, headers=headers, params=params)
            # データをJSONに変換
            json_data = res.json()

            items = json_data['messages']

            tss = []

            count = QuestionTBL.objects.all().count()

            if count > 0:
                latast_record = QuestionTBL.objects.all().count()
            else:
                latast_record = 0

            for item in items:
                if 'client_msg_id' in item:
                    if latast_record == 0:
                        tss.append(item)
                    else:
                        if QuestionTBL.objects.filter(ts=item['ts']):
                            continue
                        else:
                            tss.append(item)
            for timestamp in tss:
                TS = timestamp['ts']
                params = {
                    'channel': CHANNEL_ID,
                    'ts': TS,
                }
                res = requests.get(REPLY＿URL, headers=headers, params=params)
                json_data = res.json()
                items2 = json_data['messages']
                firstLoop = True
                latast_record = latast_record + 1
                for item2 in items2:
                    thread_ts = None
                    url = None
                    match = re.search("(?<=【)*[0-9０-９]+?(?=】)", item2['text'])
                    item2['qa_dist'] = False
                    # タイムスタンプID
                    if firstLoop:
                        if match:
                            item2['qa_dist'] = True
                            item2['postnumber'] = int(match.group())
                            item2['text'] = re.sub('(?<=【)*[0-9０-９]+?(?=】)', '', item2['text'])
                            item2['text'] = re.sub('【記事番号】', '', item2['text'])
                            # 記事番号(スプレッドシートマスタから取得)
                            ac = item2['postnumber']
                            qa = item2['qa_dist']
                            qt = item2['text']
                            b = UserMST.objects.get(user_name=item2['user'])
                            uc = b.id
                            tsdesu = item2['ts']
                            firstLoop = False
                        else:
                            continue
                    qa = item2['qa_dist']
                    qt = item2['text']
                    b = UserMST.objects.get(user_name=item2['user'])
                    uc = b.id
                    tsdesu = item2['ts']
                    ts_cd = latast_record
                    article_cd = ArticleMST.objects.get(id=ac)
                    user_cd = UserMST.objects.get(id=uc)
                    QuestionTBL.objects.filter().create(qa_dist=qa, ts=tsdesu, question_thread=qt, user_cd=user_cd,
                                                        article_cd=article_cd, ts_cd=ts_cd)

        get_channel_histry(self)
