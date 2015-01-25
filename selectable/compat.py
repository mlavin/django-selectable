"Compatibility utilites for Python/Django versions."

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
