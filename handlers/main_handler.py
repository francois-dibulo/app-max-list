# Handler for managing questions data
# @author francois@n-dream.com
import webapp2
import jinja2
from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.api import users
from models.user import User
from models.item import Item
import os
import json
import random
import re
# from models.user_helper import UserHelper
# from models.question import Question
# from models.quiz import Quiz

class MainController(webapp2.RequestHandler):

  # ---------------------------------------------------------
  # HTTP METHODS
  # ---------------------------------------------------------
  def get(self):
    template = JINJA_ENVIRONMENT.get_template('index.html')

    current_user = users.get_current_user()
    db_user = User.query(User.email == current_user.email()).fetch()
    if not db_user:
      new_user = User()
      new_user.email = current_user.email()
      new_user.put()
      memcache.flush_all()

    values = {
      "users": User().query().fetch(),
      "items": Item().query().fetch()
    }

    self.response.write(template.render(values))

    # self.response.headers['Content-Type'] = 'application/json'
    # response = []
    # params = self.request
    # item_id = self.request.get('id', None)
    # limit = self.request.get('limit', None)
    # app_key = self.request.get('app_key', None)
    # tags = self.request.get('tags', None)
    # is_public = self.request.get('is_public', "all")
    # randomize = self.request.get('randomize', False)
    # if item_id:
    #   response = self.load_by_id(item_id)
    # else:
    #   try:
    #     response = self.load_from_cache(limit=limit, is_public=is_public, tags=tags, app_key=app_key)
    #     if randomize:
    #       random.shuffle(response)
    #   except:
    #     pass
    # callback = self.request.get("callback")
    # if callback:
    #   if not re.match("^[a-zA-Z0-9\._]*$", callback):
    #     callback = ""
    # if callback:
    #   self.response.out.write(callback + "(")
    # self.response.out.write(json.dumps(response))
    # if callback:
    #   self.response.out.write(");")

  # def post(self):
    # self.response.headers['Content-Type'] = 'application/json'
    # request_data_dict = json.loads(self.request.body)
    # response = False
    # if request_data_dict:
    #   response = self.store(request_data_dict)
    # self.response.out.write(json.dumps({ "success": response }))

  # def delete(self):
    # item_id = self.request.get("id")
    # if item_id and UserHelper().is_admin():
    #   ndb.Key(Question, int(item_id)).delete()
    #   memcache.flush_all()
    # self.response.out.write(json.dumps(self.load_items()))

class UserController(webapp2.RequestHandler):

  def get(self):
    result = User.query().fetch()
    output = []
    for user in result:
      data = {
        "email": user.email
      }
      output.append(data)

    self.response.out.write(json.dumps(output))

class ItemController(webapp2.RequestHandler):

  def post(self):
    request_data_dict = self.request.body
    label = self.request.get("label", None)

    # TODO: Check if Item with label already exists
    if label:
      item = Item()
      item.label = label
      item.put()
      memcache.flush_all()

    result = {
      "success": True
    }
    self.response.out.write(json.dumps(result))

# ==========================================
# ROUTING
# ==========================================
app = webapp2.WSGIApplication([
    ('/items.*', ItemController),
    ('/users.*', UserController),
    ('/.*', MainController)
], debug=True)

JINJA_ENVIRONMENT = jinja2.Environment(
  loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
  extensions=['jinja2.ext.autoescape'],
  autoescape=True)
