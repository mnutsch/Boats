
# imports
from google.appengine.ext import ndb
import webapp2
import json

class Boat(ndb.Model):
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty()
    length = ndb.IntegerProperty()
    at_sea = ndb.BooleanProperty()

class Slip(ndb.Model):
    number = ndb.IntegerProperty(required=True)
    current_boat = ndb.StringProperty()
    arrival_date = ndb.StringProperty()
    #departure_history = ndb.StringProperty()

class BoatHandler(webapp2.RequestHandler):
    def post(self, id=None):
        #parent_key = ndb.Key(Boat, "parent_boat")
        boat_data = json.loads(self.request.body)
        new_boat = Boat(name=boat_data['name'])
        #new_boat.parent = parent_key
        new_boat.type = boat_data['type']
        new_boat.length = boat_data['length']
        new_boat.at_sea = True
        new_boat.put()
        boat_dict = new_boat.to_dict()
        boat_dict['self'] = '/boat/' + new_boat.key.urlsafe() 
        #self.response.write("post received")
        self.response.status_int = 200
        self.response.write(json.dumps(boat_dict))

    def get(self, id=None):
        if id:
            b = ndb.Key(urlsafe=id).get()
            b_d = b.to_dict()
            b_d['self'] = "/boat/" + id
            self.response.status_int = 200
            self.response.write(json.dumps(b_d))
        else:
            self.response.status_int = 200
            self.response.write("Get all request received.")
            
    def delete(self, id=None):
        if id:
            try:
                b = ndb.Key(urlsafe=id).get()

                #empty the slip the boat was previously in
                #DEV NOTE: ADD CODE HERE

                b.key.delete()
                self.response.status_int = 200
                self.response.write("Record deleted.")
            except:
                self.response.status_int = 204
                self.response.write("Record not found.")
                
        else:
            self.response.status_int = 400
            self.response.write("Delete request received, but no ID.")

    def patch(self, id=None):
        if id:
            #match the record
            b = ndb.Key(urlsafe=id).get()
            #set the values of the record from the parameters
            b.type = boat_data['type']
            b.length = boat_data['length']
            b.at_sea = boat_data['at_sea']

            #This should cause the previously occupied slip to become empty
            #DEV NOTE: ADD CODE HERE

            #update the values in the DB
            b.put()
            #respond to the client
            self.response.status_int = 200
            self.response.write("Patch request received with ID.")
        else:
            self.response.status_int = 400
            self.response.write("Patch request received, but no ID.")

class SlipHandler(webapp2.RequestHandler):
    def post(self, id=None):
        #parent_key = ndb.Key(Slip, "parent_slip")
        slip_data = json.loads(self.request.body)
        new_slip = Slip(number=slip_data['number'])
        #new_slip.parent = parent_key
        new_slip.current_boat = slip_data['current_boat']
        new_slip.arrival_date = slip_data['arrival_date']
        #new_slip.departure_history = slip_data['departure_history']
        new_slip.put()
        slip_dict = new_slip.to_dict()
        slip_dict['self'] = '/slip/' + new_slip.key.urlsafe() 
        #self.response.write("post received")
        self.response.write(json.dumps(slip_dict))

    def get(self, id=None):
        if id:
            s = ndb.Key(urlsafe=id).get()
            s_d = s.to_dict()
            s_d['self'] = "/slip/" + id
            self.response.status_int = 200
            self.response.write(json.dumps(s_d))
        else:
            self.response.status_int = 200
            self.response.write("Get all request received")
            
    def delete(self, id=None):
        if id:
            s = ndb.Key(urlsafe=id).get()

            #empty the slip the boat was previously in
            #DEV NOTE: ADD CODE HERE

            s.key.delete()
            self.response.status_int = 200
            self.response.write("Record deleted.")
        else:
            self.response.status_int = 400
            self.response.write("Delete request received, but no ID.")

    def patch(self, id=None):
        self.response.write("Patch request received")

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.status_int = 404
        self.response.write("Incorrect URL")

# Code added to allow PATCH method
# source: https://stackoverflow.com/questions/16280496/patch-method-handler-on-google-appengine-webapp2
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# [START boat]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boat', BoatHandler), #add
    ('/boat/(.*)', BoatHandler), #get
    ('/slip', SlipHandler), #add
    ('/slip/(.*)', SlipHandler) #get
], debug=True)
# [END boat]
