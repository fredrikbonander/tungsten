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
import logging

class GetHandler:
    def __init__(self, path, *args):
        args[0].path = '/' + path[0]
        args[0].lang = path[0].split('/')[0]
        self.preparePage(*args)
        self.renderPage(*args)
        
    def preparePage(self, view, query):
        pages = dbPages.Pages.all()
        view.currentPage = None
        view.pageTree = PageService.build_tree(pages, view.lang, True)
        view.pages = pages
        view.settings = Settings
        
    def renderPage(self, view, query):
        if view.path == '/' + view.lang + '/':
            view.currentPage = dbPages.Pages.gql('WHERE startpage = True').get()
            if view.currentPage is None:
                raise ValueError('Missing startpage. Select a start page under tab "Page Settings"')
            
            pageModule = dbPageModules.PageModules.gql('WHERE pageKey = :pageKey AND lang = :lang', pageKey = view.currentPage.key(), lang = view.lang).get()
        else:
            pageModule = dbPageModules.PageModules.gql('WHERE path = :path', path = view.path).get()
        
        if pageModule is None:
            raise ValueError('Missing pageModule')
        else:
            if not view.currentPage: 
                view.currentPage = dbPages.Pages.get(pageModule.pageKey.key())
            
            pageTemplateType = view.currentPage.templateType.split('.')[-1]
            pageTemplate = getattr(PageTemplates, pageTemplateType, None)
            view.pageTemplate = pageTemplate(page = view.currentPage)
            view.pageContent = view.pageTemplate.pageData[view.lang]