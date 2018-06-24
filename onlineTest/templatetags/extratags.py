from django import template

register = template.Library()


@register.filter(name='get_value')
def get_value(value, args):
    return value[args]
