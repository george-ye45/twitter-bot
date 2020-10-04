from bot_setup import TwitterBot
import time

twitter_bot = TwitterBot()

while True:
    if twitter_bot.status_update():
        twitter_bot.retweet()


