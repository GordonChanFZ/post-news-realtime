# -*- coding: utf-8 -*-
import argparse
from typing import Optional

from channel.wxpusher import WxpusherBot, FinanceBot


class BotFactory:
    @staticmethod
    def create_bot(
        name:str,app_token: str, service: str,interval: Optional[int] = None
    ) -> WxpusherBot:
        if name == "finance":
            cls=FinanceBot
        else:
            raise ValueError(f"Unknown Bot name: {name}")
        bot_instance = cls
        if not callable(bot_instance):
            raise ValueError(f"The created bot instance is not callable.")
        return bot_instance(app_token, service, interval)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Choose bot to trigger")
    parser.add_argument(
        "name", type=str, choices=["finance"], help="bot name to run"
    )
    parser.add_argument("token", type=str, help="app token")
    parser.add_argument("service", type=str, help="app or topic name")
    parser.add_argument(
        "-i", "--interval", type=int, help="trigger interval in seconds", default=None
    )

    args = parser.parse_args()
    bot = BotFactory.create_bot(args.name, args.token, args.service, args.interval)
    bot.post()
