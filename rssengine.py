# -*- coding: utf-8 -*-

# http://code.google.com/appengine/docs/python/users/overview.html

# FLOW
#
# -Login
# -Register
# -Approved
# -Login
# Add RSS
# Logout

import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app, login_required
from google.appengine.ext import db

import models

# This is a decorator to make sure users are both logged in and verified by the system.
def login_and_register ( handler_method ):
	def check_login ( self, *args ):
		user = users.get_current_user()
		if not user:
			self.redirect( users.create_login_url( self.request.uri ) )
			return
		else:
			q = db.GqlQuery( "SELECT * FROM UserModel WHERE user = :1", user )
			registered_user = q.get()
			if not registered_user:
				self.redirect( '/register' )
				return
			elif not registered_user.confirmed:
				self.redirect( '/pending' )
				return
			else:
				handler_method( self, *args )
	return check_login

class MainPage ( webapp.RequestHandler ):
	@login_and_register
	def get ( self ):
		user = users.get_current_user()
		template_values = { 'nickname': user.nickname(), 'logout': users.create_logout_url( self.request.uri )  }
		path = os.path.join( os.path.dirname( __file__ ), 'templates/index.html' )
		self.response.out.write( template.render( path, template_values ) )

class RegisterPage ( webapp.RequestHandler ):
	@login_required
	def get ( self ):
		user = users.get_current_user()
		e_users = models.UserModel.gql( "WHERE user = :1 LIMIT 1", user )
		for e_user in e_users:
			if e_user.confirmed:
				self.redirect( '/' )
				return
			else:
				self.redirect( '/pending' )
				return

		template_values = {
			'nickname': user.nickname()
		}
		path = os.path.join( os.path.dirname( __file__ ), 'templates/register.html' )
		self.response.out.write( template.render( path, template_values ) )
	
	def post ( self ):
		user = users.get_current_user()
		if user:
			e_user = models.UserModel()
			e_user.user = user
			e_user.confirmed = False
			e_user.put()
			self.redirect( '/pending' )
		else:
			self.redirect( users.create_login_url( self.request.uri ) )

class PendingPage ( webapp.RequestHandler ):
	@login_required
	def get ( self ):
		user = users.get_current_user()
		template_values = {
			'nickname': user.nickname()
		}
		path = os.path.join( os.path.dirname( __file__ ), 'templates/pending.html' )
		self.response.out.write( template.render( path, template_values ) )

class SubscriptionsPage ( webapp.RequestHandler ):
	@login_and_register
	def get ( self ):
		user = users.get_current_user()
		subscriptions = db.GqlQuery( "SELECT * FROM SubscriptionModel WHERE user = :1", user )
		template_values = {
			'nickname': user.nickname(),
			'subscriptions': subscriptions
		}
		path = os.path.join( os.path.dirname( __file__ ), 'templates/subscriptions.html' )
		self.response.out.write( template.render( path, template_values ) )

class SubscribePage ( webapp.RequestHandler ):
	@login_and_register
	def get ( self ):
		user = users.get_current_user()
		template_values = {
			'nickname': user.nickname()
		}
		path = os.path.join( os.path.dirname( __file__ ), 'templates/subscribe.html' )
		self.response.out.write( template.render( path, template_values ) )

	@login_and_register
	def post ( self ):
		
		url = self.request.get( 'url' ).lower()
		
		feeds = db.GqlQuery( "SELECT * FROM FeedModel WHERE path = :1", url )
		feed = feeds.get()
		
		if None == feed:
			feed = models.FeedModel()
			feed.path = url
			feed.put()
		
		subscriptions = db.GqlQuery( "SELECT * FROM SubscriptionModel WHERE user = :1 AND feed = :2", users.get_current_user(), feed )
		subscription = subscriptions.get()
		
		if None == subscription:
			subscription = models.SubscriptionModel()
			subscription.feed = feed
			subscription.user = users.get_current_user()
			subscription.name = self.request.get( 'name' )
			subscription.put()
		
		self.redirect( '/subscriptions' )

application = webapp.WSGIApplication(
	[
		( '/', MainPage ),
		( '/register', RegisterPage ),
		( '/pending', PendingPage ),
		( '/subscriptions', SubscriptionsPage ),
		( '/subscribe', SubscribePage )
	],
	debug=True )

def main():
	run_wsgi_app( application )

if __name__ == "__main__":
	main()