# -*- coding: utf-8 -*-

import config
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required

from decorators import login_and_register
import models

class Main ( webapp.RequestHandler ):
	@login_and_register
	def get ( self ):
		user = users.get_current_user()
		template_values = { 'nickname': user.nickname(), 'logout': users.create_logout_url( self.request.uri )  }
		path = os.path.join( config.APP_TPL_DIR, 'index.html' )
		self.response.out.write( template.render( path, template_values ) )

class Register ( webapp.RequestHandler ):
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
		path = os.path.join( config.APP_TPL_DIR, 'register.html' )
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

class Pending ( webapp.RequestHandler ):
	@login_required
	def get ( self ):
		user = users.get_current_user()
		template_values = {
			'nickname': user.nickname()
		}
		path = os.path.join( config.APP_TPL_DIR, 'pending.html' )
		self.response.out.write( template.render( path, template_values ) )