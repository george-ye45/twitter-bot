from bot_setup import TwitterBot
import time

twitter_bot = TwitterBot()

twitter_bot.status_update()
twitter_bot.retweet()
twitter_bot.get_popular_areas()

