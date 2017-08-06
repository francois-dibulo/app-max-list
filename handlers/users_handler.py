from google.appengine.api import users
import webapp2
import json
from models.user_helper import UserHelper

class UsersController(webapp2.RequestHandler):

  def get(self):
    result = UserHelper().to_json()
    self.response.out.write(json.dumps(result))

app = webapp2.WSGIApplication([
    ('/.*', UsersController)
], debug=True)
