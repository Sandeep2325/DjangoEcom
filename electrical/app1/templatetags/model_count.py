from django import template
from app1.models import *
register = template.Library()
@register.filter()
def count(value):
    #value=Product
    #for values in value:
    return value.objects.all().count()