from django import template

register = template.Library()

@register.filter
def price_converter(value):
    return "{0:.3f},00".format(int(value)/1000)