

import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey


logger = logging.getLogger('django')
    
    
IsAuthenticatedOrHasAPIKey = IsAuthenticated | HasAPIKey