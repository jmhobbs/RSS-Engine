# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

class QueueFetches ( webapp.RequestHandler ):
	def get ( self ):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write( 'Fetch' )
		#taskqueue.add(url='/worker', params={'key': key})