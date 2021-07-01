from tokenizer.settings.base import *

import os

DEBUG = os.environ.get('DEBUG_VALUE', False)
ALLOWED_HOSTS = ['primer-token.herokuapp.com', '0.0.0.0']
