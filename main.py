# -*- coding: utf-8 -*-
import schedule
from channel.wecom.finance_bot import FinanceBot
from channel.wecom.hot_research_bot import HotResearchBot
import time
from config import load_config,conf
from channel import logger

def finance(webhook, interval):
    bot = FinanceBot(webhook, interval)
    bot.post('text')

def hot_search(webhook):
    bot=HotResearchBot(webhook)
    bot.post('md')

if __name__ == "__main__":

    load_config()
    # 获取环境变量的值
    webhook = conf().get("webhook")
    interval =  conf().get("interval")

    logger.info(f"雪球每5min推送最近5min的资讯")
    schedule.every(5).minutes.do(finance, webhook[0], interval)

    logger.info("设定在8:00-20:00时间范围内每隔4小时执行一次")
    schedule.every().day.at("08:00").do(hot_search, webhook[1])
    schedule.every().day.at("12:00").do(hot_search, webhook[1])
    schedule.every().day.at("16:00").do(hot_search, webhook[1])
    schedule.every().day.at("20:00").do(hot_search, webhook[1])

    while True:
        # 运行所有已经到期的定时任务
        schedule.run_pending()
        # 等待一段时间，这里设置为1秒，可以根据实际需求调整
        time.sleep(1)


