# -*- coding: utf-8 -*-

# http://code.google.com/appengine/docs/python/users/overview.html

import config
import sys

sys.path.insert( 0, config.APP_ROOT_DIR )

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from handlers import user, feeds

application = webapp.WSGIApplication(
	[
		( '/', user.MainPage ),
		( '/register', user.RegisterPage ),
		( '/pending', user.PendingPage ),
		( '/subscriptions', feeds.SubscriptionsPage ),
		( '/subscription', feeds.SubscriptionPage ),
		( '/subscribe', feeds.SubscribePage ),
		( '/unsubscribe', feeds.UnsubscribePage )
	],
	debug=True )

def main():
	run_wsgi_app( application )

if __name__ == "__main__":
	main()