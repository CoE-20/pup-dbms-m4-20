import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Thesis(ndb.Model):
    year = ndb.IntegerProperty()
    Title = ndb.StringProperty(indexed=True)
    abstract = ndb.TextProperty(indexed=True)
    adviser = ndb.StringProperty()
    section = ndb.IntegerProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('main.html')
        
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
            check = 1
            check1 = 1
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
            check = 1
            check1 = 0

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'check': check,
            'check1': check1
        }
        self.response.write(template.render(template_values))


class APIStudentHandler(webapp2.RequestHandler):
    def get(self):
        details = Thesis.query().order(-Thesis.date).fetch()
        detail_list = []

        for detail in details:
            detail_list.append({
                'id': detail.key.urlsafe(),
                'year': detail.year,
                'Title': detail.Title,
                'abstract': detail.abstract,
                'adviser': detail.adviser,
                'section': detail.section
            })

        response = {
            'result': 'OK',
            'data': detail_list
        }
        self.response.headers['Content-Type'] = 'application.json'        
        self.response.out.write(json.dumps(response))

    def post(self):
        detail = Thesis()
        detail.year = int(self.request.get('year'))
        detail.Title = self.request.get('Title')
        detail.abstract = self.request.get('abstract')
        detail.adviser = self.request.get('adviser')
        detail.section = int(self.request.get('section'))
        detail.put()

        self.response.headers['Content-Type'] = 'application/json'
        response = {
            'result': 'OK',
            'data': {
                'id': detail.key.urlsafe(),
                'year': detail.year,
                'Title': detail.Title,
                'abstract': detail.abstract,
                'adviser': detail.adviser,
                'section': detail.section,
            }
        }
        self.response.headers['Content-Type'] = 'application/json'        
        self.response.out.write(json.dumps(response))
  

app = webapp2.WSGIApplication([
    ('/api/thesis', APIStudentHandler),
    ('/', MainPageHandler)
], debug=True)