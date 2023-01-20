from django.template import Library

register = Library()

@register.inclusion_tag('django_material_icon/icon.html')
def material_icon(icon_name):
    return {'icon_name': icon_name}
