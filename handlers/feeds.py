# -*- coding: utf-8 -*-

import config
import os

import urllib

from google.appengine.api import memcache

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp.util import login_required

from decorators import login_and_register
import models

from vendor import feedparser

class Subscriptions ( webapp.RequestHandler ):
	@login_and_register
	def get ( self ):
		user = users.get_current_user()
		subscriptions = db.GqlQuery( "SELECT * FROM SubscriptionModel WHERE user = :1", user )
		template_values = {
			'nickname': user.nickname(),
			'subscriptions': subscriptions
		}
		path = os.path.join( config.APP_TPL_DIR, 'subscriptions.html' )
		self.response.out.write( template.render( path, template_values ) )

class Subscription ( webapp.RequestHandler ):
	@login_and_register
	def get ( self ):
		user = users.get_current_user()
		subscription = db.get( db.Key( self.request.get( 'id' ) ) )

		if None == subscription or subscription.user != user:
			self.redirect( '/subscriptions' )

		template_values = {
			'id': self.request.get( 'id' ).lower(),
			'subscription': subscription
		}
		path = os.path.join( config.APP_TPL_DIR, 'subscription.html' )
		self.response.out.write( template.render( path, template_values ) )

class Subscribe ( webapp.RequestHandler ):
	@login_and_register
	def get ( self ):
		user = users.get_current_user()
		template_values = {
			'nickname': user.nickname()
		}
		path = os.path.join( config.APP_TPL_DIR, 'subscribe.html' )
		self.response.out.write( template.render( path, template_values ) )

	@login_and_register
	def post ( self ):

		url = self.request.get( 'url' ).lower().strip()

		feeds = db.GqlQuery( "SELECT * FROM FeedModel WHERE path = :1", url )
		feed = feeds.get()

		# Trial parse to see if it's really a feed & get the title
		title = "UNCHANGED"
		try:
			d = feedparser.parse( url )
			title = d.feed.title # Just check it has a title
		except Exception, e:
			# TODO: Flash message here!
			self.redirect( '/subscribe' )
			return

		if None == feed:
			# Got here. Good. Make a Feed entry.
			feed = models.FeedModel()
			feed.path = url
			feed.put()

		self.redirect( '/subscribe/confirm?' + urllib.urlencode( { 'id': str( feed.key() ), 'title': title } ) )

class SubscribeConfirm ( webapp.RequestHandler ):
	@login_and_register
	def get ( self ):
		user = users.get_current_user()
		template_values = {
			'title': self.request.get( 'title' ),
			'id': self.request.get( 'id' )
		}
		path = os.path.join( config.APP_TPL_DIR, 'subscribe_confirm.html' )
		self.response.out.write( template.render( path, template_values ) )

	@login_and_register
	def post ( self ):

		feed = db.get( db.Key( self.request.get( 'id' ) ) )
		if feed == None:
			# TODO: Flash error!
			self.redirect( '/subscribe' )

		subscriptions = db.GqlQuery( "SELECT * FROM SubscriptionModel WHERE user = :1 AND feed = :2", users.get_current_user(), feed )
		subscription = subscriptions.get()

		if None == subscription:
			subscription = models.SubscriptionModel()
			subscription.feed = feed
			subscription.user = users.get_current_user()
			subscription.name = self.request.get( 'name' )
			subscription.put()

		self.redirect( '/subscriptions' )

class Unsubscribe ( webapp.RequestHandler ):
	@login_and_register
	def get ( self ):
		user = users.get_current_user()
		subscription = db.get( db.Key( self.request.get( 'id' ) ) )

		if None == subscription or subscription.user != user:
			self.redirect( '/subscriptions' )

		subscription.delete()

		template_values = {
			'id': self.request.get( 'id' ).lower(),
			'subscription': subscription
		}
		path = os.path.join( config.APP_TPL_DIR, 'unsubscribe.html' )
		self.response.out.write( template.render( path, template_values ) )