from DataFactory import dbPages
from google.appengine.ext import db

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