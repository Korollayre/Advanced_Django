from django import template

register = template.Library()


@register.filter(name='media_folder_products')
def media_folder_products(value):
    return f'/media/{value}'
