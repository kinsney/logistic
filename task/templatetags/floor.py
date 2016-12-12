from django import template
register = template.Library()
@register.filter
def floor(value,arg):
    if len(value.__str__().split('-')) == 1:
        return value.__str__()
    else:
        return value.__str__().split('-')[arg]
