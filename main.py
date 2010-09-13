#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os

from google.appengine.dist import use_library
import ImageStore

use_library('django', '1.1')

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from PageController import EditView

import Utils
import cgi

def render_template(file, template_vals):
    path = os.path.join(os.path.dirname(__file__), 'templates', file)
    return template.render(path, template_vals)

class EditHandler(webapp.RequestHandler):    
    def get(self, *path):
        view = Utils.dictObj()
        query = cgi.FieldStorage()
        EditView.GetHandler(path, view, query)
        
        self.response.out.write(render_template(view.templateFile, view))

    def post(self, *path):
        view = Utils.dictObj()
        
        EditView.PostHandler(path, view, self.request)
        
        self.redirect(view.redirect)

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(render_template('pages/main.html', {}))


def main():
    application = webapp.WSGIApplication([('/edit/action/AddUpdateImageStore', ImageStore.AddUpdateImageStore),
                                          (r'/(?i)(Edit)/(.*)', EditHandler),
                                          ('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

webapp.template.register_template_library('TemplateTags')


if __name__ == '__main__':
    main()
