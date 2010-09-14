'''
Created on Sep 9, 2010

@author: broken
'''
from DataFactory import dbPages
from DataFactory import dbPageModules
from PageService import PageTemplates
import PageService
import Settings
import Utils
from google.appengine.api import memcache

class GetHandler:
    def __init__(self, path, *args):
        args[0].path = '/' + path[0]
        args[0].lang = path[0].split('/')[0]
        self.preparePage(*args)
        self.renderPage(*args)
        
    def preparePage(self, view, query):
        # Get all pages and order by sort index
        pages = dbPages.Pages.gql('ORDER BY sortIndex').fetch(1000)
        # Get all published page modules to be match agaisnt pages
        pageModules = dbPageModules.PageModules.gql('WHERE lang = :lang AND published = :published', lang = view.lang, published = True).fetch(100)
        # Set up memcacheid based on language
        memcacheid = "mainView_pageTree_%s" % (view.lang)
        pageTree = memcache.get(memcacheid)
        # If pageTree is not in memcache, build pageTree and store it in memcache
        if pageTree is None:
            pageTree = PageService.build_tree(pages, pageModules = pageModules) 
            memcache.add(memcacheid, pageTree, Settings.memcacheTimeout)
        
        # Set currentPage to None as a precaution
        view.currentPage = None
        # Bind pageTree to view
        view.pageTree = pageTree
        
#        How to get pagecontainer items
#        footerPageContainer = dbPages.Pages.get_by_key_name('footermenu')
#        footerPages = dbPages.Pages.gql('WHERE parentKey = :parentKey', parentKey = footerPageContainer.key()).fetch(100)
#        view.footerTree = PageService.build_tree(footerPages, pageRoot = footerPageContainer)
        # Bind pages to view
        view.pages = pages
        
    def renderPage(self, view, query):
        # If we are at root page in URL
        if view.path == '/' + view.lang + '/':
            view.currentPage = dbPages.Pages.gql('WHERE startpage = True').get()
            # We need at least one page as startpage
            if view.currentPage is None:
                raise ValueError('Missing startpage. Select a start page under tab "Page Settings"')
            # Get page modules associated with startpage
            pageModule = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey AND lang = :lang', pageKey = view.currentPage.key(), lang = view.lang).get()
        else:
            # Get page modules associated with url path
            pageModule = dbPageModules.PageModules.gql('WHERE path = :path', path = view.path).get()
        # We need atleast one pageModule to display any page
        if pageModule is None:
            raise ValueError('Missing pageModule')
        else:
            # If no current page is set, set pageModules's page as currentpage
            if not view.currentPage: 
                view.currentPage = dbPages.Pages.get(pageModule.pageKey.key())
            
            # templateType is stored with entire class path, we only need the last name 
            pageTemplateType = view.currentPage.templateType.split('.')[-1]
            # Find pageTemplate class
            pageTemplateClass = getattr(PageTemplates, pageTemplateType, None)
            # Set up memcacheid based on language
            memcacheid = "mainView_pageTemplate_%s" % (view.lang)
            pageTemplate = memcache.get(memcacheid)
            # If pageTemplate is not in memcache, invoke class and store it in memcache
            if pageTemplate is None:
                pageTemplate = pageTemplateClass(page = view.currentPage)
                memcache.add(memcacheid, pageTemplate, Settings.memcacheTimeout)
            
            # Bind pageTemplate to view
            view.pageTemplate = pageTemplate
            view.pageContent = view.pageTemplate.pageData[view.lang]