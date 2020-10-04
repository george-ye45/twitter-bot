import tweepy
import os
from dotenv import load_dotenv
import random
from datetime import datetime, date

load_dotenv()

class TwitterBot:
    def __init__(self):
        self.CONSUMER_KEY = os.getenv('CONSUMER_KEY')
        self.CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
        self.ACCESS_KEY = os.getenv('ACCESS_KEY')
        self.ACCESS_SECRET = os.getenv('ACCESS_SECRET')
        self.api = None
        self.days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
        self.categories = ["Politics", "Science", "Entertainment"]
        self.prev_category = None
        self.category = None
        self.set_API()
    
    def set_API(self):
        auth = tweepy.OAuthHandler(self.CONSUMER_KEY, self.CONSUMER_SECRET)
        auth.set_access_token(self.ACCESS_KEY, self.ACCESS_SECRET)
        self.api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    def status_update(self):
        self.prev_category = self.category
        new_category = None
        while new_category == None or new_category == self.prev_category:
            new_category = random.choice(self.categories)
        self.category = new_category
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == "12:00:00":
            current_day = self.days[date.today().weekday()]
            return self.api.update_status("%s news! Today's Topic: %s" % (current_day, category))

    def search(self):
        all_results = (self.api.search(q = self.category, count = 5, lang = 'en', result_type = 'popular')['statuses'])
        result_ids = []
        for i in all_results:
            result_ids.append(i['id'])
        print(self.category)
        return result_ids
    
    def retweet(self):
        print("Retweeting")
        id_list = self.search()
        for tweet in id_list:
            try:
                return None
                #self.api.retweet(tweet)
            except NameError:
                print(NameError)


