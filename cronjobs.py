# -*- coding: utf-8 -*-

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

class Queue ( webapp.RequestHandler ):
	def get ( self ):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write( 'Fetch' )
		#taskqueue.add(url='/worker', params={'key': key})

application = webapp.WSGIApplication(
	[
	( '/cron/queue', Queue )
	],
	debug=True )

def main ():
	run_wsgi_app( application )

if __name__ == "__main__":
	main()