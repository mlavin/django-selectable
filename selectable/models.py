from django.conf import settings

# Set default settings
if not hasattr(settings, 'SELECTABLE_MAX_LIMIT'):
    settings.SELECTABLE_MAX_LIMIT = 25
