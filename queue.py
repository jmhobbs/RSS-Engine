# -*- coding: utf-8 -*-

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# http://code.google.com/appengine/docs/python/urlfetch/fetchfunction.html
# http://code.google.com/appengine/docs/python/mail/sendingmail.html

class FetchRSS ( webapp.RequestHandler ):
	def post ( self ):
		key = self.request.get( 'key' )
		return

class SendMail (webapp.RequestHandler):
	def post ( self ):
		key = self.request.get( 'key' )
		return

application = webapp.WSGIApplication(
	[
		( '/queue/fetch', FetchRSS ),
		( '/queue/mail', SendMail ),
	],
	debug=True
)

def main ():
	run_wsgi_app( application )

if __name__ == '__main__':
		main()