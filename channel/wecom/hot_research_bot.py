# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List
from urllib.parse import quote
import requests
from channel import logger
from channel.utils import Message
from channel.wecom.wecom_topic import WecomTopicBot


class HotResearchBot(WecomTopicBot):

    def get_messages(self) -> List[Message]:
        news_list = self.get_hot()
        timestamp=int(datetime.timestamp(datetime.now()))
        messages = []
        if news_list:
            for news in news_list:
                messages.append(
                    Message(text=news,published_at=timestamp)
                )
        return messages

    @classmethod
    def get_hot(cls) -> List[str]:
        url = 'https://weibo.com/ajax/side/hotSearch'
        logger.info("Query news from Weibo")
        response = requests.get(url)

        news_list = []
        top10=''
        if response.status_code == 200:
            data = response.json()['data']
            print(data)
            top10+=datetime.now().strftime('微博热搜榜')+'\n'
            pushTop=data['hotgov']['word'].strip('#')
            top10+=f'<font color=\"warning\">**置顶**：</font>{pushTop}\n'
            for i, rs in enumerate(data['realtime'][:10], 1):
                title = rs['word']
                try:
                    label = rs['label_name']
                    if label in ['新', '热', '新']:
                        label = f'<font color=\"warning\">{label}</font>'
                    else:
                        label = ''
                except:
                    label = ''
                top10+=f"{i}. [{title}](https://s.weibo.com/weibo?q={quote(title)}&Refer=top) {label} \n"
            top10+=datetime.now().strftime('\(%Y-%m-%d %H:%M\)')
        else:
            logger.warning("获取微博热搜榜失败")
            logger.error(response.text)
        news_list.append(top10)
        return news_list

