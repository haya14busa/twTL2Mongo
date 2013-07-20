#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from app.model import Tweet
from mongoengine import *

import secret
 
 
def getOauth():
    CONSUMER_KEY=secret.CONSUMER_KEY
    CONSUMER_SECRET=secret.CONSUMER_SECRET
    ACCESS_TOKEN_KEY=secret.ACCESS_TOKEN_KEY
    ACCESS_TOKEN_SECRET=secret.ACCESS_TOKEN_SECRET
 
    auth = OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessKey, accessSecret)
    return auth
 
 
class AbstructListener(StreamListener):
    def on_status(self, status):
        model = Tweet()
        model.name = status.author.name
        model.user_id = status.author.id
        model.screen_name = status.author.screen_name
        model.text = status.text
        model.icon_path = status.author.profile_image_url
        model.created_at = status.created_at
        model.save()
 
if __name__ == '__main__':
    db = connect('tweetstream')
    print db
    auth = getOauth()
    stream = Stream(auth, AbstructListener(), secure=True)
    stream.filter(track='python')
