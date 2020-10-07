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

    # Update status based on day and category
    def status_update(self):
        self.prev_category = self.category
        new_category = None
        while new_category == None or new_category == self.prev_category:
            new_category = random.choice(self.categories)
        self.category = new_category
        current_day = self.days[date.today().weekday()]
        return self.api.update_status("%s news! Today's Topic: %s" % (current_day, self.category))

    # Searches top 5 popular tweets based on some category and returns a list of the tweets IDs
    def search(self):
        all_results = (self.api.search(q = self.category, count = 5, lang = 'en', result_type = 'popular')['statuses'])
        result_ids = []
        for i in all_results:
            result_ids.append(i['id'])
        print(self.category)
        return result_ids
    
    # Retweets the 5 most popular tweets if they have not already been retweeted
    def retweet(self):
        id_list = self.search()
        for tweet in id_list:
            try:
                self.api.retweet(tweet)
            except NameError:
                print(NameError)

    # Print the top 5 most popular countries and their tweet count
    # You will only be able to do this once every 15 minutes due to Twitter's rate limit on getting trends API
    def get_popular_areas(self):
        all_places = self.api.trends_available()
        place_popularity = {}
        record = []
        for i in all_places:
            if i['country'] in record:
                continue
            trends_list = self.api.trends_place(i['woeid'])[0]['trends']
            max_tweets = self.get_max_tweets(trends_list)
            if i['country'] == '':
                i['country'] = "WorldWide"
            place_popularity[i['country']] = max_tweets
            record.append(i['country'])
        sorted_places = sorted(place_popularity.items(), key = lambda x: x[1], reverse=True)
        print("Here are the top 10 most popular countries by tweets currently!")
        for i in range(5):
            print(sorted_places[i][0], sorted_places[i][1])
    
    # Helper function for get_popular_areas(). Find max tweet count in a list of trends
    def get_max_tweets(self, trends):
        max_tweet = 0
        for trend in trends:
            if trend['tweet_volume'] == None:
                trend['tweet_volume'] = 0
            if trend['tweet_volume'] > max_tweet:
                max_tweet = trend['tweet_volume']
        return max_tweet
