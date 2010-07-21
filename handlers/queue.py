# -*- coding: utf-8 -*-

import config

import datetime
import time

from google.appengine.ext import db
from google.appengine.ext import webapp

import models

from vendor import feedparser

class FetchRSS ( webapp.RequestHandler ):
	def post ( self ):
		feed = db.get( db.Key( self.request.get( 'key' ) ) )

		fetch = models.FetchModel()
		fetch.feed = feed
		try:
			d = feedparser.parse( feed.path )
			story_time = datetime.datetime.fromtimestamp( time.mktime( d.entries[0].updated_parsed ) )
			if feed.last_story != None and story_time > feed.last_story:
				# TODO: Parse stories!
				fetch.new_stories = 1
			else:
				fetch.new_stories = 0
			fetch.success = True
			feed.last_fetch = datetime.datetime.now()
			feed.put()
		except:
			run_diff = datetime.timedelta(
				days=config.FETCH_INTERVAL['days'],
				hours=config.FETCH_INTERVAL['hours'],
				minutes=config.FETCH_INTERVAL['minutes']
			)
			feed.last_fetch = feed.last_fetch + diff
			feed.put()
			fetch.new_stories = 0
			fetch.success = False
		fetch.put()

class SendMail (webapp.RequestHandler):
	# http://code.google.com/appengine/docs/python/mail/sendingmail.html
	def post ( self ):
		key = self.request.get( 'key' )
		return