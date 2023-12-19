# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
from channel.wecom.finance_bot import FinanceBot

if __name__ == "__main__":
    # 加载当前目录下的.env文件
    load_dotenv()

    # 获取环境变量的值
    webhook = os.environ.get("WEBHOOK")
    interval = int(os.environ.get("INTERVAL"))

    bot=FinanceBot(webhook,interval)
    bot.post()
