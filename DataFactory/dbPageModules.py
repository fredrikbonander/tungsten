'''
Created on Sep 9, 2010

@author: broken
'''
from google.appengine.ext import db
from DataFactory import dbPages

class PageModules(db.Model):
    '''
    classdocs
    '''
    lang = db.StringProperty()
    path = db.StringProperty()
    published = db.BooleanProperty(default=False)
    parentKey = db.ReferenceProperty(dbPages.Pages)
    
    @property
    def itemid(self):
        return self.key().id()