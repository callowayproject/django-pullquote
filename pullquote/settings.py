from django.conf import settings

TEMPLATES = getattr(settings, "PULLQUOTE_TEMPLATES", {})

CACHE_TIMEOUT = getattr(settings, "PULLQUOTE_CACHE_TIMEOUT", 60)

CACHE_PREFIX = getattr(settings, "PULLQUOTE_CACHE_PREFIX", "PQ")