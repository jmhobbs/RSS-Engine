# -*- coding: utf-8 -*-

import config

import logging # TODO: Use logging.
import datetime

from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api.labs import taskqueue

import models

class QueueFetches ( webapp.RequestHandler ):
	def get ( self ):
		now = datetime.datetime.now()
		diff = datetime.timedelta(
			days=config.FETCH_INTERVAL['days'],
			hours=config.FETCH_INTERVAL['hours'],
			minutes=config.FETCH_INTERVAL['minutes']
		)
		then = now + diff
		feeds = db.GqlQuery( "SELECT * FROM FeedModel WHERE last_fetch <= :1", then )
		total = 0
		for feed in feeds:
			# TODO: Check if in queue already?
			task = taskqueue.Task( url='/queue/fetch', params={ 'key': feed.key() } )
			task.add( "fetch" )
			total += 1
		self.response.out.write( "Queued up %d fetches." % total )
		logging.debug( "Queued up %d fetches." % total )