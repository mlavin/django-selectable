"Compatibility utilites for Python/Django versions."
import sys

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
else:
    string_types = basestring,

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module
