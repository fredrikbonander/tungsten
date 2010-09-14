'''
Created on Sep 9, 2010

@author: broken
'''
from PageService import PageTypes

class PageContainer(PageTypes.PageType):
    templateName = 'PageContainer'
    
    def __init__(self):
        pass

class StandardPage(PageTypes.PageType):
    # Display name in EDIT/new page
    templateName = 'StandardPage'
    templateFile = 'pages/standardpage.html'
    
    def addModules(self):
        self.modules.append(PageTypes.getStandardHeading(self, 'MainHeading'))
        self.modules.append(PageTypes.getStandardTextBox(self, 'MainTextBox'))
        self.modules.append(PageTypes.getImageListModule(self, 'ImageList'))