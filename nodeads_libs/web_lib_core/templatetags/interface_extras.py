from django import template

register = template.Library()


def check_translation(value, default):
    return value if value else default


register.filter('chk', check_translation)
