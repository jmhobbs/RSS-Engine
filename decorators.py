# -*- coding: utf-8 -*-

from google.appengine.api import users
from google.appengine.ext import db

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