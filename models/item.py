from google.appengine.ext import ndb
import json

class Item(ndb.Model):
  label = ndb.StringProperty()
  created_at = ndb.DateTimeProperty(auto_now_add=True)
