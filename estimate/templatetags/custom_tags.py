from django.views.generic import CreateView
from roman import toRoman
from django.template.defaultfilters import register
from string import ascii_lowercase as letters


@register.filter
def roman(value):
    if value and value > 0:
        return toRoman(value)