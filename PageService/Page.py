from DataFactory import dbPages
from DataFactory import dbContentModules
from DataFactory import dbPageModules
from google.appengine.ext import db
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
    
    pageKey = db.put(page)
    
    return { 'status' : 1, 'message' : 'Page added/updated', 'pageId' : str(pageKey.id()) }

def GetPath(page, lang, path):
    if page.parentKey == None:
        return '/' + lang + '/' + path
    else:
        page = dbPages.Pages.get(page.parentKey.key())
        pageModule = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey AND lang = :lang', pageKey = page.key(), lang = lang).get()
        
        if pageModule is None:
            return False
        
        return pageModule.path + path

def AddUpdateContent(params):
    args = params.arguments()
    #isModule = re.compile("^(module_)") 
    #isDynamicModuel = re.compile("^(dynamic_)") 
    pageKey = db.Key(params.get('pageKey'))
    pageModuleName = params.get('page_module_name')
    lang = params.get('lang')
        
    if params.get('publish') == "on":
        publish = True 
    else: 
        publish = False
    
    page = dbPages.Pages.get(pageKey)
    pageModule = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey AND lang = :lang', pageKey = pageKey, lang = lang).get()
    
    if pageModule is None:
        pageModule = dbPageModules.PageModules() 
        pageModule.pageKey = pageKey
        pageModule.lang = lang
        
    pageModule.name = pageModuleName
    stringPath = Utils.slugify(unicode(pageModuleName)) + '/'
    path = GetPath(page, lang, stringPath)
    
    ## If path is False, parent page in GetPath method has not been saved.
    if not path:
        return { 'status' : -1, 'message' : 'Parent page is not published', 'pageId' : str(page.key().id()) }
    
    pageModule.path = path
    pageModule.published = publish
    
    pageModuleKey = db.put(pageModule)
        
    for arg in args:
        argList = arg.split('|')
        if len(argList) > 1:
            # Save only static modules
            if argList[1] == 'static' or argList[1] == 'imageList':
                contentModule = dbContentModules.ContentModules.gql('WHERE pageModuleKey = :pageModuleKey AND name = :name', pageModuleKey = pageModuleKey, name = argList[0]).get()
                
                if contentModule is None:
                    contentModule = dbContentModules.ContentModules()
                    contentModule.pageModuleKey = pageModuleKey
                    contentModule.name = argList[0]
                    
                contentModule.content = params.get(arg)
                    
                db.put(contentModule)
    
    return { 'status' : 1, 'message' : 'Content added/updated', 'pageId' : str(page.key().id()) }