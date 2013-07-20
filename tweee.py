#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from app.model import Tweet
from mongoengine import *
 
 
def getOauth():
    consumerKey = 'consumerkey'
    consumerSecret = 'consumer secret'
    accessKey = 'access key'
    accessSecret = 'access secret'
 
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
