from DataFactory import dbPages
from DataFactory import dbContentModules
from DataFactory import dbPageModules
from google.appengine.ext import db
import logging
import re
import Utils

def AddOrUpdate(params):
    if not params.get('page_id'):
        page = dbPages.Pages()
        
    page.name = params.get('page_name')
    page.templateType = params.get('page_templateType')
    page.sortIndex = int(params.get('page_sortIndex'));
    
    parentKey = None
        
    if int(params.get('page_parent')):
        parentKey = dbPages.Pages.get_by_id(int(params.get('page_parent'))).key()
    
    page.parentKey = parentKey
    
    db.put(page)
    
    return { 'status' : 1, 'message' : 'Page added/updated' }

def AddUpdateContent(params):
    args = params.arguments()
    #isModule = re.compile("^(module_)") 
    #isDynamicModuel = re.compile("^(dynamic_)") 
    pageKey = db.Key(params.get('pageKey'))
    pageModuleName = params.get('page_module_name')
    lang = params.get('lang')
    
    if params.get('publish') == "on":
        publish =  True 
    else: 
        publish = False
    
    pageModule = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey AND lang = :lang', pageKey = pageKey, lang = lang).get()
    
    if pageModule is None:
        pageModule = dbPageModules.PageModules() 
        pageModule.pageKey = pageKey
        pageModule.lang = lang
        
    pageModule.name = pageModuleName
    pageModule.path = Utils.slugify(unicode(pageModuleName))
    pageModule.published = publish
    
    pageModuleKey = db.put(pageModule)
        
    for arg in args:
        argList = arg.split('|')
        if len(argList) > 1:
            if argList[1] == 'static':
                contentModule = dbContentModules.ContentModules.gql('WHERE pageModuleKey = :pageModuleKey AND name = :name', pageModuleKey = pageModuleKey, name = argList[0]).get()
                
                if contentModule is None:
                    contentModule = dbContentModules.ContentModules()
                    contentModule.pageModuleKey = pageModuleKey
                    contentModule.name = argList[0]
                    
                contentModule.content = params.get(arg)
                    
                db.put(contentModule)
    
    return { 'status' : 1, 'message' : 'Content added/updated' }