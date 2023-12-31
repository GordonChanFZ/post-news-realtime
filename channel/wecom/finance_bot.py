# -*- coding: utf-8 -*-
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import List

import requests
from requests.cookies import RequestsCookieJar

from channel import logger
from channel.wecom.wecom_topic import WecomTopicBot
from channel.utils import escape_text, Message



@dataclass(frozen=True)
class FinanceNews:
    """新闻信息的数据封装类"""

    id: int
    text: str
    mark: int
    target: str = field(repr=False)
    created_at: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FinanceNews):
            return NotImplemented
        return self.id == other.id

    def to_markdown(self) -> str:
        return f"""
{escape_text(self.text)}

{escape_text(datetime.fromtimestamp(self.created_at / 1000, tz=timezone(timedelta(hours=8))).strftime('(%Y-%m-%d %H:%M)'))}
"""
    #兼容微信，微信不支持md格式
    def to_text(self) -> str:
        return f"""{self.text}
{datetime.fromtimestamp(self.created_at / 1000, tz=timezone(timedelta(hours=8))).strftime('(%Y-%m-%d %H:%M)')}
"""


class FinanceBot(WecomTopicBot):
    requests_headers = {
        "User-Agent": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:70.0) Gecko/20100101 Firefox/70.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://xueqiu.com/today/",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    }

    def get_messages(self) -> List[Message]:
        news_list = self.get_news()
        messages = []
        if news_list:
            # 按照时间先后排序
            news_list.reverse()
            for news in news_list:
                messages.append(
                    Message(text=news.to_text(), published_at=news.created_at)
                )
        return messages

    @classmethod
    def get_news(cls) -> List[FinanceNews]:
        url = "https://xueqiu.com/v4/statuses/public_timeline_by_category.json"
        logger.info("Query news from XueQiu")
        response = requests.get(
            url,
            params={"since_id": -1, "max_id": -1, "count": 10, "category": 6},
            headers=cls.requests_headers,
            cookies=cls.get_cookie(),
        )
        news_list = []
        if response.status_code == 200:
            for item in response.json().get("list", []):
                item = json.loads(item["data"])
                news_list.append(
                    FinanceNews(
                        id=item["id"],
                        text=item["text"],
                        mark=item["mark"],
                        target=item["target"],
                        created_at=item["created_at"],
                    )
                )
        else:
            logger.warning("Get news failed")
            logger.error(response.text)
        return news_list

    @classmethod
    def get_cookie(cls) -> RequestsCookieJar:
        logger.info("get cookies")
        url = "https://xueqiu.com/?category=livenews"
        response = requests.get(url, headers=cls.requests_headers)
        return response.cookies

