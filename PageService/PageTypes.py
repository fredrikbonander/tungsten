'''
Created on Sep 9, 2010

@author: broken
'''
def parsePageData(data):
    dataAsDict = {}
    if data:
        for entry in data:
            if entry.dynamicModules is not None and entry.content is None:
                dataAsDict[entry.name] = entry.dynamicModules
            elif entry.content is None:
                dataAsDict[entry.name] = ''
            else:
                dataAsDict[entry.name] = entry.content
                    
    return dataAsDict

class PageType():
    def __init__(self):
        self.pageData = parsePageData()
        self.modules = []
    
    def addModules(self):
        pass
    
    def renderEditPage(self):
        self.addModules()
        return self.modules
    
def getStandardHeading(template, name):
    templateData = ''
    if name in template.pageData:
        templateData = template.pageData[name]
        
    return { 'name' : name, 'type' : 'static', 'file' : 'module_heading.html', 'data' : templateData }

def getStandardTextBox(template, name):
    templateData = ''
    if name in template.pageData:
        templateData = template.pageData[name]
        
    return { 'name' : name, 'type' : 'static', 'file' : 'module_textbox.html', 'data' : templateData }