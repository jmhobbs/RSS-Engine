# -*- coding: utf-8 -*-

# http://code.google.com/appengine/docs/python/users/overview.html

# FLOW
#
# Login
# Register
# Approved
# Login
# Add RSS
# Logout

import os
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class EngineUser ( db.Model ):
	user = db.UserProperty()
	confirmed = db.BooleanProperty()
	created = db.DateTimeProperty(auto_now_add=True)

class MainPage ( webapp.RequestHandler ):
	def get ( self ):
		user = users.get_current_user()
		if user:
			template_values = { 'nickname': user.nickname() }
			path = os.path.join( os.path.dirname( __file__ ), 'templates/index.html' )
			self.response.out.write( template.render( path, template_values ) )
		else:
			self.redirect( users.create_login_url( self.request.uri ) )

class RegisterPage ( webapp.RequestHandler ):
	def get ( self ):
		user = users.get_current_user()
		if user:
			e_users = EngineUser.gql( "WHERE user = :1 LIMIT 1", user )
			for e_user in e_users:
				if e_user.confirmed:
					self.redirect( '/' )
				else:
					self.redirect( '/pending' )

			template_values = {
				'nickname': user.nickname()
			}
			path = os.path.join( os.path.dirname( __file__ ), 'templates/register.html' )
			self.response.out.write( template.render( path, template_values ) )
		else:
			self.redirect( users.create_login_url( self.request.uri ) )
	
	def post ( self ):
		user = users.get_current_user()
		if user:
			e_user = EngineUser()
			e_user.user = user
			e_user.confirmed = False
			e_user.put()
			self.redirect( '/pending' )
		else:
			self.redirect( users.create_login_url( self.request.uri ) )

class PendingPage ( webapp.RequestHandler ):
	def get ( self ):
		user = users.get_current_user()
		if user:
			template_values = {
				'nickname': user.nickname()
			}
			path = os.path.join( os.path.dirname( __file__ ), 'templates/pending.html' )
			self.response.out.write( template.render( path, template_values ) )
		else:
			self.redirect( users.create_login_url( self.request.uri ) )

application = webapp.WSGIApplication(
	[
		( '/', MainPage ),
		( '/register', RegisterPage ),
		( '/pending', PendingPage )
	],
	debug=True )

def main():
	run_wsgi_app( application )

if __name__ == "__main__":
	main()