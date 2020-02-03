from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def analytics_id():
    return getattr(settings, 'ANALYTICS_ID', '')

@register.simple_tag
def analytics_cookie_domains():
    return getattr(settings, 'ANALYTICS_COOKIE_DOMAINS', [])
