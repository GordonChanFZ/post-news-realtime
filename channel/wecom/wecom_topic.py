#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import time
from typing import List, Optional
import requests
from channel import logger
from channel.utils import Message
from channel.chatgpt_bot import ChatGPTBot

class WecomTopicBot:

    def __init__(self, webhook: str, interval: Optional[int] = None):
        self.webhook = webhook
        self.headers={'Content-Type': 'application/json'}
        self.interval = interval
        self.start_time = int(time.time() * 1000)

    def _send_message_text(
            self, message
    ) -> None:
        # wecom_example = {
        #     "msgtype": "text",
        #     "text": {
        #         "content": "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意."
        #     }
        # }
        response = requests.post(
            url=self.webhook,
            headers=self.headers,
            data=json.dumps({
                "msgtype": "text",
                "text": {
                    "content": str(message)
                }
            }),
        )

        # 判断请求是否成功，并记录日志
        if response.status_code == 200:
            logger.info('消息发送成功')
            logger.info(response.text)
        else:
            logger.error('消息发送失败')

    def _send_message_md(
            self, message
    ) -> None:
        # wecom_example = {
        #     "msgtype": "text",
        #     "text": {
        #         "content": "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意."
        #     }
        # }
        logger.info(str(message))
        response = requests.post(
            url=self.webhook,
            headers=self.headers,
            data=json.dumps({
                "msgtype": "markdown",
                "markdown": {
                    "content":str(message)
                }
            }),
        )

        # 判断请求是否成功，并记录日志
        if response.status_code == 200:
            logger.info('消息发送成功')
            logger.info(response.text)
        else:
            logger.error('消息发送失败')

    def _bulk_send_messages(
            self, messages: List[Message],type:str
    ) -> None:
        for message in messages:
            if self.is_message_expired(message):
                logger.info(f"Ignore expired message: {message}")
                continue
            if type == 'text':
                self._send_message_text(message)
            if type == 'md':
                self._send_message_md(message)

    def post(
            self,type:str
    ) -> None:
        messages = self.get_messages()
        self._bulk_send_messages(messages,type)

    def get_messages(self) -> List[Message]:
        raise NotImplementedError

    def is_message_expired(self, message: Message) -> bool:
        if self.interval is None:
            return False
        if self.start_time - self.interval * 1000 <= message.published_at:
            return False
        return True

if __name__=='__main__':
    response = requests.post(
        url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=3c3568b9-0402-4953-bb08-0dd0abafa0ce',
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            "msgtype": "text",
            "text": {
                "content": 'test'
            }
        }),
    )

    # 判断请求是否成功，并记录日志
    if response.status_code == 200:
        logger.info('消息发送成功')
        logger.info(response.text)
    else:
        logger.error('消息发送失败')