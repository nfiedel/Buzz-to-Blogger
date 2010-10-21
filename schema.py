
from google.appengine.ext import db



class SomeUpdate(db.Model):
  """Some topic update.
  
  Key name will be a hash of the feed source and item ID.
  """
  title = db.TextProperty()
  content = db.TextProperty()
  updated = db.DateTimeProperty(auto_now_add=True)
  link = db.TextProperty()


class UserStuff(db.Model):
    user = db.UserProperty()
    authToken = db.StringProperty()
    blogId = db.StringProperty()
    buzzFeed = db.StringProperty()
