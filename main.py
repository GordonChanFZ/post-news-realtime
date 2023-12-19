# -*- coding: utf-8 -*-
import schedule
import argparse
from channel.wecom.finance_bot import FinanceBot
import time
def job(webhook, interval):
    bot = FinanceBot(webhook, interval)
    bot.post()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Choose bot to trigger")
    parser.add_argument(
        "name", type=str, choices=["finance"], help="bot name to run"
    )
    parser.add_argument("webhook", type=str, help="webhook")
    parser.add_argument(
        "-i", "--interval", type=int, help="trigger interval in seconds", default=None
    )

    args = parser.parse_args()
    # 获取环境变量的值
    webhook = args.webhook
    interval =  args.interval

    print(f"定义定时任务，每5min执行")
    schedule.every(5).minutes.do(job,webhook,interval)

    while True:
        # 运行所有已经到期的定时任务
        schedule.run_pending()
        # 等待一段时间，这里设置为1秒，可以根据实际需求调整
        time.sleep(1)


