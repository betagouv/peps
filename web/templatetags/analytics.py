from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def analytics_id():
    return getattr(settings, 'ANALYTICS_ID', '')

@register.simple_tag
def analytics_cookie_domain():
    return getattr(settings, 'ANALYTICS_COOKIE_DOMAIN')

@register.simple_tag
def analytics_domain():
    return getattr(settings, 'ANALYTICS_DOMAIN')
