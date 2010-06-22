# -*- coding: utf-8 -*-

from google.appengine.ext import db

# [ User ]<-->[ Subscriptions ]<-->[ Feed ]<-->[ Fetch ]
#                                    ^-->[ Story ]

class UserModel ( db.Model ):
	user = db.UserProperty()
	confirmed = db.BooleanProperty()
	created = db.DateTimeProperty( auto_now_add=True )

class FeedModel ( db.Model ):
	path = db.StringProperty()
	last_fetch = db.DateTimeProperty( auto_now_add=True )

class SubscriptionModel ( db.Model ):
	feed = db.ReferenceProperty( FeedModel )
	user = db.UserProperty()
	name = db.StringProperty()
	created = db.DateTimeProperty( auto_now_add=True )

class FetchModel ( db.Model ):
	feed = db.ReferenceProperty( FeedModel )
	ran = db.DateTimeProperty( auto_now_add=True )
	success = db.BooleanProperty()

class StoryModel ( db.Model ):
	feed = db.ReferenceProperty( FeedModel )
	captured = db.DateTimeProperty( auto_now_add=True )
	created = db.DateTimeProperty( auto_now_add=True )
	title = db.StringProperty()
	author = db.StringProperty()
	content = db.TextProperty()