

import os
import environ
env = environ.Env()
environ.Env.read_env()


# SECURITY WARNING: don't run with debug turned on in production!
ENV = os.getenv('ENV', default=env('ENV'))

if ENV == 'PROD':
    from cbers_cc.production_settings import *
else:
    from cbers_cc.base_settings import *