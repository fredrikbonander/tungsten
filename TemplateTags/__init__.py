import os
from django.template import Library, Node, TemplateSyntaxError
from google.appengine.ext import webapp
import logging

register = webapp.template.create_template_register()

def PageTree(pages):
    return  { 'pageTree' : pages }

path = os.path.join(os.path.dirname(__file__), '../templates/edit/pageTree.html')
register.inclusion_tag(path)(PageTree)

def Module(module, language):
    data = ''
    if module['data'].has_key(language):
        data = module['data'][language]
    return  { 'module' : module, 'data' : data }

path = os.path.join(os.path.dirname(__file__), '../templates/edit/modules/module.html')
register.inclusion_tag(path)(Module)

def ifIn(value, list):
    if value in list:
        return True
    else:
        return False
    
register.filter('ifIn', ifIn)