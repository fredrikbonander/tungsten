'''
Created on Sep 13, 2010

@author: broken
'''
from google.appengine.ext import db

class ImageStore(db.Model):
    name = db.StringProperty()
    description = db.TextProperty()
    imageUrl = db.StringProperty()
    
    @property
    def itemId(self):
        return self.key().id()
