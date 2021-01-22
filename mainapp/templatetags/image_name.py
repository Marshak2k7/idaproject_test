import os
from django import template

register = template.Library()


@register.filter
def image_name(value):
    return os.path.basename(value.name)
