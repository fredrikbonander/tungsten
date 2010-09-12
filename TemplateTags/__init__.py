import os
from django.template import Node
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

class GetDictKey(Node):
    def __init__(self, args):
        self.args = args

    def render(self, context):
        logging.info(self.args)
        return self.args[1][self.args[2]][self.args[3]]

def getDictKey(parser, token):
    logging.info(parser)
    logging.info(token)
    args = token.contents.split()
    return GetDictKey(args)
    
register.tag('getDictKey', getDictKey)