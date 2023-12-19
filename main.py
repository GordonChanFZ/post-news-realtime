# -*- coding: utf-8 -*-
import argparse
from typing import Optional

from channel.wecom.wecom_topic import WecomTopicBot
from channel.wecom.finance_bot import FinanceBot


class BotFactory:
    @staticmethod
    def create_bot(
        name:str,webhook: str,interval: Optional[int] = None
    ) -> WecomTopicBot:
        if name == "finance":
            cls=FinanceBot
        else:
            raise ValueError(f"Unknown Bot name: {name}")
        return cls(webhook,  interval)




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
    bot = BotFactory.create_bot(args.name, args.webhook, args.interval)
    bot.post()
