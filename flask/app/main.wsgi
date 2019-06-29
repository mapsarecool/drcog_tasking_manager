#!/usr/bin/python3.6

import logging
import sys
import os
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/app/')

from main import app as application
# This can be any value, just using th TM consumer secret, since we have it
application.secret_key = os.environ['TM_CONSUMER_SECRET']

print('application')
print (application.run())
