
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from gdata import service
import gdata
import gdata.alt.appengine
import atom
import common

def GetAuthSubUrl():
  next = '%s/auth' % common.GetBaseUri()
  #'http://localhost:8080/auth'
  scope = 'http://www.blogger.com/feeds'
  secure = False
  session = True
  blogger_service = service.GDataService()
  gdata.alt.appengine.run_on_appengine(blogger_service)
  return blogger_service.GenerateAuthSubURL(next, scope, secure, session);


class MainPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            self.response.headers['Content-Type'] = 'text/html'
            authUrl = GetAuthSubUrl()
            self.response.out.write('Hello. Click <a href="%s">here</a> to auth.' % authUrl)
            self.response.out.write('<div><a href="%s">logout</a></div>' % users.create_logout_url('/'))
        else:
            self.redirect(users.create_login_url(self.request.uri))
