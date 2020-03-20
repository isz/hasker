from django.template import Library

register = Library()

@register.filter(name='page_range') 
def times(number):
    return range(1,number+1)