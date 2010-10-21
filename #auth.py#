
import os
from google.appengine.ext.webapp import template

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import gdata.blogger.service
import gdata.alt.appengine
from gdata.auth import AuthSubToken
import gdata
import atom
import re


from xml.dom import minidom 

from google.appengine.api import urlfetch
from google.appengine.ext import db

from schema import UserStuff

import urllib


def FetchBuzzApiUrl(email):
    url = "http://www.google.com/s2/webfinger/?q=%s" % email
    result = urlfetch.fetch(url)

    XRD_NS = 'http://docs.oasis-open.org/ns/xri/xrd-1.0'
    dom = minidom.parseString(result.content)
    for node in dom.getElementsByTagNameNS(XRD_NS, 'Link'):
        if 'http://schemas.google.com/g/2010#updates-from' == node.getAttribute('rel'):
            return node.getAttribute('href')
    return ''


def SubscribePubsubHubbub(feedUrl):
    url='http://pubsubhubbub.appspot.com/subscribe'
    fields = {
        'hub.callback': 'http://buzztoblogger.appspot.com/subscriber',
        'hub.mode': 'subscribe',
        'hub.verify': 'async',
        'hub.topic': feedUrl,
        }
    headerset = { 'Content-Type': 'application/x-www-form-urlencoded' }
    form_data = urllib.urlencode(fields)
    result = urlfetch.fetch(url=url,
                            payload=form_data,
                            method=urlfetch.POST,
                            headers=headerset)
    return result.status_code


class PickBlogHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        currentUser = users.get_current_user()
        if currentUser:
            query = UserStuff.all()
            query.filter('user =', currentUser)
            results = query.fetch(limit=1)
            userStuff = results[0]
            updatedBlogId = self.request.get('blogid')

            buzzFeedUrl = FetchBuzzApiUrl(currentUser.email())
            subscribeResponseCode = SubscribePubsubHubbub(buzzFeedUrl)
            if 202 == subscribeResponseCode:
                self.response.out.write('PubSubHubbub Subscribe succeeded for feed %s.<br/>' % buzzFeedUrl)

            if updatedBlogId:
                userStuff.blogId = updatedBlogId
                userStuff.buzzFeed = buzzFeedUrl
                userStuff.put()
                self.response.out.write('<div>Set BlogId</div>')


            # no longer echo the token as it's 'secure'
            self.response.out.write('All done. You can close this app now.')
            self.response.out.write('<br/>Debug info: user %s, blogId %s' % (userStuff.user.email(), userStuff.blogId))
        else:
            self.redirect(users.create_login_url(self.request.uri))

class AuthHandler(webapp.RequestHandler):
    def get(self):
        currentUser = users.get_current_user()
        if currentUser:
            self.response.headers['Content-Type'] = 'text/html'

            self.blogger =  gdata.blogger.service.BloggerService()
            gdata.alt.appengine.run_on_appengine(self.blogger)
            
            authTok =  gdata.auth.extract_auth_sub_token_from_url(self.request.uri)
            self.blogger.SetAuthSubToken(authTok)
            
            self.blogger.UpgradeToSessionToken(authTok)
            self.blogger.SetAuthSubToken(authTok.get_token_string())
            sessionTok = self.blogger.GetAuthSubToken()
            # DEBUG ONLY:
            # self.response.out.write('Updated AuthTok= %s, SessionTok = %s' % (authTok, sessionTok))
 
            feed = self.blogger.GetBlogFeed()
            
            template_values = {
                'title': feed.title.text,
                'entries': feed.entry,
            }

            path = os.path.join(os.path.dirname(__file__), 'auth.html')
            self.response.out.write(template.render(path, template_values))


            userStuff = UserStuff()
            userStuff.user = currentUser
            userStuff.authToken = authTok.get_token_string()
            userStuff.put()
        else:
            self.redirect(users.create_login_url(self.request.uri))
