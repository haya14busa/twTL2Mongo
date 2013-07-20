#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://dev.hageee.net/10
 
import json
from datetime import datetime
from flask import Flask, Response
from mongoengine import *
from app.model import Tweet, db
 
app = Flask(__name__)
 
 
@app.route('/api')
def getTweet():
    datas = []
    with db:
        tweets = Tweet.objects.order_by('-created_at').limit(100)
        for tweet in tweets:
            created_at = datetime.strftime(tweet.created_at, '%Y/%m/%d %H:%M:%S')
            datas.append({'name': tweet.screen_name, 'text': tweet.text, 'icon_path': tweet.icon_path, 'created_at': created_at})
    try:
        res = json.dumps(datas)
    except Exception:
        raise
    return Response(res, content_type="application/json", status=200)
 
if __name__ == '__main__':
    app.run()
