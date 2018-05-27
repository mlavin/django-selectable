"Compatibility utilites for Python/Django versions."

try:
    from urllib.parse import urlparse
except ImportError:
    # This can be removed when Python 2.7 support is dropped
    from urlparse import urlparse

try:
    from django.urls import reverse
except ImportError:
    # This can be removed when Django < 1.9 support is dropped
    from django.core.urlresolvers import reverse
