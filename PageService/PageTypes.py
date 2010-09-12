'''
Created on Sep 9, 2010

@author: broken
'''
from DataFactory import dbPageModules
from DataFactory import dbContentModules
import logging
def parsePageData(data):
    dataAsDict = {}
    if data:
        for lang in data:
            dataAsDict[lang] = {}
            for entry in data[lang]:
                if entry.content is None:
                    dataAsDict[lang][entry.name] = ''
                else:
                    dataAsDict[lang][entry.name] = entry.content
                    
    return dataAsDict

class PageType():
    def __init__(self, **kwargs):
        #db.get([DataFactory.dbPages.Pages.get_value_for_datastore(cartItem) for cartItem in cartItemsData ])
        #page = DataFactory.dbPages.Pages.get_by_id(int(kwargs['pageId']))
        page = kwargs['page']
        pageKey = page.key()
        
        pageModuleList = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey', pageKey = pageKey).fetch(1000)
        pageData = {}
        pageModules = {}
        for pageModule in pageModuleList:
            pageModules[pageModule.lang] = pageModule
            pageData[pageModule.lang] = dbContentModules.ContentModules.gql('WHERE pageModuleKey = :pageModuleKey', pageModuleKey = pageModule.key()).fetch(100)
        
        self.pageModules = pageModules
        self.pageKey = pageKey
        self.pageData = parsePageData(pageData)
        self.modules = []
    
    def addModules(self):
        pass
    
    def renderEditPage(self):
        self.addModules()
    
def getStandardHeading(template, name):
    templateData = {}
    for lang in template.pageData:
        if name in template.pageData[lang]:
            templateData[lang] = template.pageData[lang][name]
        
    return { 'name' : name, 'type' : 'static', 'file' : 'modules/module_heading.html', 'data' : templateData }

def getStandardTextBox(template, name):
    templateData = {}
    for lang in template.pageData:
        if name in template.pageData[lang]:
            templateData[lang] = template.pageData[lang][name]
        
    return { 'name' : name, 'type' : 'static', 'file' : 'modules/module_textbox.html', 'data' : templateData }