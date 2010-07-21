# -*- coding: utf-8 -*-

# This is how often a feed should be fetched (if it succeeds each time)
# Do this in negative values. So every 2 hours is represented as -2 hours
FETCH_INTERVAL = { 'days': 0, 'hours': -2, 'minutes': 0 }

# This is how long a failed feed should wait to retry. Positive values here.
RETRY_INTERVAL = { 'days': 0, 'hours': 0, 'minutes': 30 }

DEBUG=True

## You shouldn't need to modify anything below this line. ##

import os

VERSION="0.1.0"

APP_ROOT_DIR = os.path.abspath( os.path.dirname( __file__ ) )
APP_TPL_DIR = os.path.join( APP_ROOT_DIR, 'templates/' )