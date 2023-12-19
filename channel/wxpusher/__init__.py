#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import logging
import time
from typing import List, Optional
import requests
from channel import logger
from channel.utils import Message
from channel.chatgpt_bot import ChatGPTBot

class WxpusherBot:

    def __init__(self, app_token: str, service: str,interval: Optional[int] = None):
        self.app_token = app_token
        self.service=service
        self.uids = self.get_wxuser_info()
        self.interval = interval
        self.start_time = int(time.time() * 1000)

    # post_example_json = {
    #     "appToken": "AT_xxx",
    #     "content": "Wxpusher祝你中秋节快乐!",
    #     "summary": "消息摘要",  # 消息摘要，显示在微信聊天页面或者模版消息卡片上，限制长度100，可以不传，不传默认截取content前面的内容。
    #     "contentType": 1,  # 内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown
    #     "topicIds": [  # 发送目标的topicId，是一个数组！！！，也就是群发，使用uids单发的时候， 可以不传。
    #         123
    #     ],
    #     "uids": [  # 发送目标的UID，是一个数组。注意uids和topicIds可以同时填写，也可以只填写一个。
    #         "UID_xxxx"
    #     ],
    #     "url": "https://wxpusher.zjiecode.com",  # 原文链接，可选参数
    #     "verifyPay": False  # 是否验证订阅时间，true表示只推送给付费订阅用户，false表示推送的时候，不验证付费，不验证用户订阅到期时间，用户订阅过期了，也能收到。
    # }

    def _send_message(
            self, message
    ) -> None:
        prompt = '帮我总结如下这段内容，请简要回复，不超过20个字'
        summary = ChatGPTBot().chatgpt(prompt=prompt, message=message)
        #print(summary)
        response = requests.post(
            url='https://wxpusher.zjiecode.com/api/send/message',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                "appToken": self.app_token,
                "content": message,
                "summary": summary,
                "contentType": 3,
                "uids": self.uids,
                "verifyPay": False
            }),
        )

        # 判断请求是否成功，并记录日志
        if response.status_code == 200:
            logging.info('消息发送成功')
            logging.info(response.text)
        else:
            logging.error('消息发送失败')

    def _bulk_send_messages(
            self, messages: List[Message]
    ) -> None:
        for message in messages:
            if self.is_message_expired(message):
                logger.info(f"Ignore expired message: {message}")
                continue
            self._send_message(str(message))

    def post(
            self
    ) -> None:
        messages = self.get_messages()
        self._bulk_send_messages(messages)

    def get_messages(self) -> List[Message]:
        raise NotImplementedError

    def is_message_expired(self, message: Message) -> bool:
        if self.interval is None:
            return False
        if self.start_time - self.interval * 1000 <= message.published_at:
            return False
        return True

    def get_wxuser_info(self, page=1, page_size=100, uid=None, is_block=False, user_type=0):
        # 请求参数
        params = {
            "appToken": self.app_token,  # appToken 应用密钥标志
            "page": page,  # page 请求数据的页码
            "pageSize": page_size,  # pageSize 分页大小，不能超过100
            "uid": uid,  # uid 用户的uid，可选，如果不传就是查询所有用户，传uid就是查某个用户的信息。
            "isBlock": is_block,  # isBlock 查询拉黑用户，可选，不传查询所有用户，true查询拉黑用户，false查询没有拉黑的用户
            "type": user_type  # type 关注的类型，可选，不传查询所有用户，0是应用，1是主题。 返回数据：
        }

        # 发送GET请求
        response = requests.get('https://wxpusher.zjiecode.com/api/fun/wxuser/v2', params=params)

        # user_lisuser_list = {
        #     "code": 1000,
        #     "msg": "处理成功",
        #     "data": {
        #         "total": 40,  # 总数
        #         "page": 1,  # 当前页码
        #         "pageSize": 20,  # 页码大小，
        #         "records": [
        #             {
        #                 "uid": "UID_xxx",  # 用户uid
        #                 "appOrTopicId": 111,  # 用户关注的应用或者主题id，根据type来区分
        #                 "headImg": "",  # 新用户微信不再返回 ，强制返回空
        #                 "createTime": 1603540859285,  # 创建时间
        #                 "nickName": "",  # 新用户微信不再返回 ，强制返回空
        #                 "reject": False,  # 是否拉黑
        #                 "id": 47361,  # id，如果调用删除或者拉黑接口，需要这个id
        #                 "type": 0,  # 关注类型，0：关注应用，1：关注topic
        #                 "target": "WxPusher官方",  # 关注的应用或者主题名字
        #                 "payEndTime": 0  # 0表示用户不是付费用户，大于0表示用户付费订阅到期时间，毫秒级时间戳
        #             }
        #         ]
        #     },
        #     "success": True
        # }

        # 解析响应结果
        if response.status_code == 200:
            logging.info('获取用户UID列表成功')
            data = response.json()
            if data['msg'] == '处理成功':
                users = data['data']['records']
                users_uid = [user['uid'] for user in users if user.get('target') == self.service]
                return users_uid
        else:
            logging.error('获取用户UID列表失败')

        return []

from .finance_bot import FinanceBot
if __name__ == '__main__':
    self = WxpusherBot('AT_djGMF6vWGdTZDyaXBLXFVPtU3HAxtaFD','7*24news', 300)
    print(self.get_wxuser_info())
    uids=self.get_wxuser_info()
    data={
            "appToken": self.app_token,
            "content": "【大商所、郑商所夜盘收盘 PX涨超1%】大商所、郑商所夜盘收盘，涨多跌少。棕榈油、PX等涨超1%，菜粕、纯碱等小幅上涨；玉米跌超1%，玻璃、焦煤等小幅下跌。上期所LU燃油涨超3%。",
            "summary": "7*24news",
            "contentType": 2,
            "uids": uids,
            "verifyPay": False
        }
    response = requests.post(
        url='https://wxpusher.zjiecode.com/api/send/message',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(data),
    )

    # 判断请求是否成功，并记录日志
    if response.status_code == 200:
        logging.info('消息发送成功', response.text)
    else:
        logging.error('消息发送失败')

