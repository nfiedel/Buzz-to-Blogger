
import auth
import mainpage
import subscriber


from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

application = webapp.WSGIApplication(
  [
    ('/', mainpage.MainPage),

    (r'/auth/pickblog', auth.PickBlogHandler),
    (r'/auth.*', auth.AuthHandler),

    # Subscriber Handlers
    (r'/subscriber/items', subscriber.ItemsHandler),
    (r'/subscriber/debug', subscriber.DebugHandler),
    # Wildcard below so we can test multiple subscribers in a single app.
    (r'/subscriber.*', subscriber.InputHandler),
    (r'/subscriber/view', subscriber.ViewHandler),
  ],
  debug=True)


def main():
  wsgiref.handlers.CGIHandler().run(application)



def main():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
