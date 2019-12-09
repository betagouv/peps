from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def ga_id():
    return getattr(settings, 'GOOGLE_ANALYTICS_ID', '')
