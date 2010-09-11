'''
Created on Sep 9, 2010

@author: broken
'''
from google.appengine.ext import db
from DataFactory import dbPageModules

class ContentModules(db.Model):
    name = db.StringProperty()
    content = db.TextProperty()
    pageModule = db.ReferenceProperty(dbPageModules.PageModules)
    
    @property
    def itemid(self):
        return self.key().id()