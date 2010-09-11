import os
from google.appengine.ext import webapp

register = webapp.template.create_template_register()

def PageTree(pages):
    return  { 'pageTree' : pages }

path = os.path.join(os.path.dirname(__file__), '../templates/edit/pageTree.html')
register.inclusion_tag(path)(PageTree)