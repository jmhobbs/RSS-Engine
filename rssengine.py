# -*- coding: utf-8 -*-

# http://code.google.com/appengine/docs/python/users/overview.html

import config
import sys

sys.path.insert( 0, config.APP_ROOT_DIR )

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from handlers import user, feeds, content

application = webapp.WSGIApplication(
	[
		( '/', content.Home ),
		( '/register', user.Register ),
		( '/pending', user.Pending ),
		( '/subscriptions', feeds.Subscriptions ),
		( '/subscription', feeds.Subscription ),
		( '/subscribe', feeds.Subscribe ),
		( '/subscribe/confirm', feeds.SubscribeConfirm ),
		( '/unsubscribe', feeds.Unsubscribe ),
		( '/.*', content.FourOhFour )
	],
	debug=config.DEBUG )

def main():
	run_wsgi_app( application )

if __name__ == "__main__":
	main()