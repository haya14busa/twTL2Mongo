#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from tweepy.streaming import StreamListener, Stream
from tweepy.auth import OAuthHandler
from app.model import Tweet
from mongoengine import *

import secret
from datetime import timedelta
import urllib
import logging
 
 
def getOauth():
    CONSUMER_KEY=secret.CONSUMER_KEY
    CONSUMER_SECRET=secret.CONSUMER_SECRET
    ACCESS_TOKEN_KEY=secret.ACCESS_TOKEN_KEY
    ACCESS_TOKEN_SECRET=secret.ACCESS_TOKEN_SECRET
 
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    return auth
 
 
class AbstructListener(StreamListener):
    def on_status(self, status):
        try:
            model = Tweet()
            model.name = status.author.name
            model.user_id = status.author.id
            model.screen_name = status.author.screen_name
            model.text = status.text
            model.icon_path = status.author.profile_image_url
            model.created_at = status.created_at + timedelta(hours=9) # add 9 hours for Japanese time
            model.source = status.source
            model.id_str = status.id_str
            model.in_reply_to_status_id_str = status.in_reply_to_status_id_str

            model.save()
        except:
            pass


 
 
class UserStream(Stream):
  
    def user_stream(self, follow=None, track=None, async=False, locations=None):
        self.parameters = {"delimited": "length", }
        self.headers['Content-type'] = "application/x-www-form-urlencoded"
 
        if self.running:
            raise TweepError('Stream object already connected!')
 
        self.scheme = "https"
        self.host = 'userstream.twitter.com'
        self.url = '/2/user.json'
 
        if follow:
           self.parameters['follow'] = ','.join(map(str, follow))
        if track:
            self.parameters['track'] = ','.join(map(str, track))
        if locations and len(locations) > 0:
            assert len(locations) % 4 == 0
            self.parameters['locations'] = ','.join(['%.2f' % l for l in locations])
 
        self.body = urllib.urlencode(self.parameters)
        logging.debug("[ User Stream URL ]: %s://%s%s" % (self.scheme, self.host, self.url))
        logging.debug("[ Request Body ] :" + self.body)
        self._start(async)

if __name__ == '__main__':
    db = connect('tweetstream')
    print db
    auth = getOauth()
    # stream = Stream(auth, AbstructListener(), secure=True)
    # stream.filter(track='python')
    stream = UserStream(auth, AbstructListener(), secure=True)
    stream.timeout = None
    stream.user_stream()
