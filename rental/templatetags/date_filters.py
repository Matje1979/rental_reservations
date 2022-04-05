from django import template

register = template.Library()


@register.filter(name="date_iso")
def date_iso(value):
    return value.isoformat()
