"Compatibility utilites for Python/Django versions."
import sys

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

try:
    from django.utils.encoding import smart_text, force_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text
    from django.utils.encoding import force_unicode as force_text

try:
    from django.forms.utils import flatatt
except ImportError:
    from django.forms.util import flatatt

PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
else:
    string_types = basestring,

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

try:
    from django.apps import AppConfig
    LEGACY_AUTO_DISCOVER = False
except ImportError:
    LEGACY_AUTO_DISCOVER = True
