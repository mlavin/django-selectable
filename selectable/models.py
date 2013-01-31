from __future__ import unicode_literals

from django.conf import settings

# Set default settings
if not hasattr(settings, 'SELECTABLE_MAX_LIMIT'):
    settings.SELECTABLE_MAX_LIMIT = 25

if not hasattr(settings, 'SELECTABLE_ESCAPED_KEYS'):
    settings.SELECTABLE_ESCAPED_KEYS = ('label', )
