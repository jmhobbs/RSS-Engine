# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.ext import webapp

# http://code.google.com/appengine/docs/python/urlfetch/fetchfunction.html
# http://code.google.com/appengine/docs/python/mail/sendingmail.html

class FetchRSS ( webapp.RequestHandler ):
	def post ( self ):
		key = self.request.get( 'path' )
		return

class SendMail (webapp.RequestHandler):
	def post ( self ):
		key = self.request.get( 'key' )
		return