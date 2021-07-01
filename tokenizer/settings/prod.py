from tokenizer.settings.base import *
import os
import django_heroku

DEBUG = os.environ.get('DEBUG_VALUE', False)
ALLOWED_HOSTS = ['primer-token.herokuapp.com', '0.0.0.0']

django_heroku.settings(locals())
