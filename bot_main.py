from bot_setup import TwitterBot
import time

twitter_bot = TwitterBot()

while True:
    print("in loop")
    twitter_bot.status_update()
    twitter_bot.retweet()
    time.sleep(5)


