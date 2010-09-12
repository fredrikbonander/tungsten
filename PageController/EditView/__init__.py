'''
Created on Sep 9, 2010

@author: broken
'''
from DataFactory import dbPages
from PageService import PageTemplates
from PageService import Page
from PageService.PageTypes import PageType

import Users
import Utils
import PageService
import logging
import Settings

class GetHandler:
    def __init__(self, path, *args):
        self.pathList = Utils.parsePath(path[1])
        
        if not Users.isUserAuthenticated():
            args[0].templateFile = 'edit/login.html'
        else:
            func = getattr(self, self.pathList[0])
            func(*args)

    def getPageData(self, view, pageId):
        currentPage = dbPages.Pages.get_by_id(int(pageId))
        pageTemplateType = currentPage.templateType.split('.')[-1]
        pageTemplate = getattr(PageTemplates, pageTemplateType, None)
        view.pageTemplate = pageTemplate(page = currentPage)
        view.pageTemplate.addModules()
                
    def main(self, view, query):
        pages = dbPages.Pages.all()
        view.pageTree = PageService.build_tree(pages)
        view.pages = pages
        view.settings = Settings        
        
        if query.getvalue('pageId'):
            self.getPageData(view, query.getvalue('pageId'))
        
        view.templateTypes = Utils.getPageTemplates(PageTemplates, PageType)
        view.templateFile = 'edit/' + self.pathList[0] + '.html'
        
class PostHandler:
    def __init__(self, path, *args):
        self.pathList = Utils.parsePath(path[1])
        func = getattr(self, self.pathList[1])
        func(*args)

    def login(self, view, post):
        view.StatusMessage = Users.doLogin(post.get('username'), post.get('password'))
        view.redirect = '/edit/'
        
        if view.StatusMessage['status'] < 0:
            view.redirect = '/edit/?message=' + view.StatusMessage['message'] 
      
    def AddUpdatePage(self, view, post):
        view.StatusMessage = Page.AddOrUpdate(post)
        view.redirect = '/edit/'
        
        if view.StatusMessage['status'] < 0:
            view.redirect = '/edit/?message=' + view.StatusMessage['message']
            
    def AddUpdateContent(self, view, post):
        view.StatusMessage = Page.AddUpdateContent(post)
        view.redirect = '/edit/'
        
        if view.StatusMessage['status'] < 0:
            view.redirect = '/edit/?message=' + view.StatusMessage['message']
        