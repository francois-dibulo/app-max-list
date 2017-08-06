from google.appengine.ext import ndb
import json

class User(ndb.Model):
  name = ndb.StringProperty()
  email = ndb.StringProperty()
  created_at = ndb.DateTimeProperty(auto_now_add=True)
