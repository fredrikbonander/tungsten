'''
Created on Sep 9, 2010

@author: broken
'''

from google.appengine.api import blobstore
from DataFactory import dbPages, dbImageStore
from PageService import PageTemplates
from PageService import Page
from PageService.PageTypes import PageType

import Users
import Utils
import PageService
import Settings

class GetHandler:
    def __init__(self, path, *args):
        self.pathList = Utils.parsePath(path[1])
        
        args[0].statusCode = args[1].getvalue('status')
        args[0].statusMessage = args[1].getvalue('message')
        
        if not Users.isUserAuthenticated():
            args[0].templateFile = 'edit/login.html'
        else:
            self.preparePage(*args)
            func = getattr(self, self.pathList[0])
            func(*args)
    
    def preparePage(self, view, query):
        pages = dbPages.Pages.all()
        view.currentPage = None
        view.pageTree = PageService.build_tree(pages)
        view.pages = pages
        view.settings = Settings

    def getPageData(self, view, pageId):
        view.currentPage = dbPages.Pages.get_by_id(int(pageId))
        pageTemplateType = view.currentPage.templateType.split('.')[-1]
        pageTemplate = getattr(PageTemplates, pageTemplateType, None)
        view.pageTemplate = pageTemplate(page = view.currentPage)
        view.pageTemplate.addModules()
        view.imageList = dbImageStore.ImageStore.all()
    
    def newpage(self, view, query):
        view.templateTypes = Utils.getPageTemplates(PageTemplates, PageType)
        view.templateFile = 'edit/' + self.pathList[0] + '.html'
    
    def imageStore(self, view, query):
        if query.getvalue('imageId'):
            view.currentImage = dbImageStore.ImageStore.get_by_id(int(query.getvalue('imageId')))
            view.currentImageDescription = dbImageStore.ImageDescription.gql('WHERE imageEntry = :imageEntry', imageEntry = view.currentImage.key())
        
        view.uploadUrl = blobstore.create_upload_url('/edit/action/AddUpdateImageStore')
        view.imageList = dbImageStore.ImageStore.all()
        view.templateTypes = Utils.getPageTemplates(PageTemplates, PageType)
        view.templateFile = 'edit/' + self.pathList[0] + '.html'
        
    def main(self, view, query):
        if query.getvalue('pageId'):
            self.getPageData(view, query.getvalue('pageId'))
        
        view.templateFile = 'edit/' + self.pathList[0] + '.html'
        
class PostHandler:
    def __init__(self, path, *args):
        self.pathList = Utils.parsePath(path[1])
        func = getattr(self, self.pathList[1])
        func(*args)        

    def login(self, view, post):
        view.StatusMessage = Users.doLogin(post.get('username'), post.get('password'))
        view.redirect = '/edit/?status=' + str(view.StatusMessage['status'])  + '&message=' + view.StatusMessage['message']
      
    def AddUpdatePage(self, view, post):
        view.StatusMessage = Page.AddOrUpdate(post)
        view.redirect = '/edit/?pageId=' + view.StatusMessage['pageId'] + '&status=' + str(view.StatusMessage['status'])  + '&message=' + view.StatusMessage['message']
            
    def AddUpdateContent(self, view, post):
        view.StatusMessage = Page.AddUpdateContent(post)
        view.redirect = '/edit/?pageId=' + view.StatusMessage['pageId'] + '&status=' + str(view.StatusMessage['status'])  + '&message=' + view.StatusMessage['message']
     
    def AddUpdatePageSettings(self, view, post):
        view.StatusMessage = Page.AddUpdatePageSettings(post)
        view.redirect = '/edit/?pageId=' + view.StatusMessage['pageId'] + '&status=' + str(view.StatusMessage['status'])  + '&message=' + view.StatusMessage['message']
        
    def DeletePage(self, view, post):
        view.StatusMessage = Page.DeletePage(post)
        
        if view.StatusMessage['pageId'] == '0':
            view.redirect = '/edit/newpage/?status=' + str(view.StatusMessage['status'])  + '&message=' + view.StatusMessage['message']
        else:
            view.redirect = '/edit/?pageId=' + view.StatusMessage['pageId'] + '&status=' + str(view.StatusMessage['status'])  + '&message=' + view.StatusMessage['message']