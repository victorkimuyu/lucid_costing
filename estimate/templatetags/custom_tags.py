import roman
from django.template.defaultfilters import register
from string import ascii_lowercase as letters


@register.filter
def to_roman(value):
    if value:
        return roman.toRoman(value)


@register.filter
def to_letter(value):
    if value and value < 26:
        return letters[value-1]
