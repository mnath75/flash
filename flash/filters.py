from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def format_timedelta(value):
    hours, remainder = divmod(value.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"