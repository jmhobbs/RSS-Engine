# -*- coding: utf-8 -*-
import config
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

class Home ( webapp.RequestHandler ):
	def get ( self ):
		path = os.path.join( config.APP_TPL_DIR, 'index.html' )
		self.response.out.write( template.render( path, () ) )

class FourOhFour ( webapp.RequestHandler ):
	def get ( self ):
		path = os.path.join( config.APP_TPL_DIR, '404.html' )
		self.response.out.write( template.render( path, () ) )