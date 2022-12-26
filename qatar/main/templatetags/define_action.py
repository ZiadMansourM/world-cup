from django import template
register = template.Library()

@register.simple_tag
def define(row, col, taken_seats):
    return (row, col) in taken_seats