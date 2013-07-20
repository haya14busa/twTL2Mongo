#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
from mongoengine import *
 
 
class Tweet(Document):
    name = StringField()
    user_id = IntField()
    screen_name = StringField()
    text = StringField()
    icon_path = StringField()
    cached_icon_path = StringField()
    created_at = DateTimeField()
 
 
class DBI(object):
    def __init__(self):
        self.db = None
 
    def __enter__(self):
        self.connect()
 
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            self.db = None
            return False
        self.close()
        self.db = None
        return True
 
    def close(self):
        self.db.disconnect()
        print self.db, "closed"
 
    def connect(self):
        self.db = connect('tweetstream')
        print self.db, "connected"
 
db = DBI()
