"Compatibility utilites for Python versions."

try:
    from urllib.parse import urlparse
except ImportError:
    # This can be removed when Python 2.7 support is dropped
    from urlparse import urlparse
