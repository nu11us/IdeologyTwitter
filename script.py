import os
import json
import GetOldTweets3 as got
#import tweepy
from datetime import datetime
import time

def last_month(month_string):
    year, month = month_string.split("-")
    year, month = int(year), int(month)
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    if month >= 10:
        return "{}-{}".format(year,month)
    else:
        return "{}-0{}".format(year,month)

def next_month(month_string):
    year, month = month_string.split("-")
    year, month = int(year), int(month)
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    if month >= 10:
        return "{}-{}".format(year,month)
    else:
        return "{}-0{}".format(year,month)

class UserElement:
    def __init__(self, name, json = None):
        self.id = name
        self.json = json
        self.dir = "twl/{}/".format(name)
        if self.json != None:
            self.data = self.import_json(json)
        else:
            self.data = None

    def import_json(self, json):
        pass

    def get_metadata(self):
        pass
    
    def get_data(self):
        metadata = self.get_metadata()

    def get_num_tweets(self):
        today = datetime.today().strftime("%Y-%m")
        month = last_month(today)
        while os.path.exists(self.dir + "{}-{}.csv".format(self.id,month)):
            month = last_month(month)
        month = next_month(month)
        num = 0
        while month != datetime.today().strftime("%Y-%m"):
            with open(self.dir + "{}-{}.csv".format(self.id,month), "r", errors='ignore') as csv:
                num -= 1
                for line in csv:
                    num += 1
            month = next_month(month)
        return num
      
    def get_tweets(self, month):
        header = "date,username,to,replies,retweets,favorites,text,geo,mentions,hashtags,id,permalink"
        while month != datetime.today().strftime("%Y-%m"):
            tweet_search = got.manager.TweetCriteria()\
                .setUsername(self.id)\
                .setSince("{}-01".format(month))\
                .setUntil("{}-01".format(next_month(month)))\
                .setEmoji("unicode")
            if not os.path.exists(self.dir + "{}-{}.csv".format(self.id,month)):
                tweets = got.manager.TweetManager.getTweets(tweet_search)
                with open(self.dir + "{}-{}.csv".format(self.id,month), "w+", encoding="utf-8") as csv:
                    csv.write(header+'\n')
                    for tweet in tweets:
                        csv.write(tweet.date.strftime("%Y-%m-%d %H:%M:%S") + ",")
                        csv.write(tweet.username + ",")
                        csv.write(tweet.to or "" + ",")
                        csv.write(str(tweet.replies) + ",")
                        csv.write(str(tweet.retweets) + ",")
                        csv.write(str(tweet.favorites) + ",")
                        csv.write(tweet.text + ",")
                        csv.write(tweet.geo + ",")
                        csv.write(tweet.mentions + ",")
                        csv.write(tweet.hashtags + ",")
                        csv.write(tweet.id + ",")
                        csv.write(tweet.permalink + "\n")
            
                print("{}-{}.csv".format(self.id,month))
                month = next_month(month)    
                time.sleep(5)

class TweetLibrary:
    def __init__(self, directory=""):
        self.dir = directory+"twl/"
        self.data = []

    def get_prexisting_users(self):
        if os.path.exists(self.dir):
            users = [i.rstrip() for i in open(self.dir+"users").readlines()]
            for user in users:
                elem = UserElement(name, self.dir+"{}/metadata.json".format(name))
                self.data.append(elem)

    def add_user(self):
        pass

user = UserElement("guardian") 
user.get_tweets("2014-11")