from django import template
import re

register = template.Library()


@register.filter
def replace(value, arg):
    """
    Replaces the value with arg
    """
    if value is None:
        value = ''
    return str(value).replace(arg, '')


@register.filter
def replace_placeholders(html, context_dict):
    """
    Replaces placeholders in the format {placeholder} with values from the context_dict
    """
    if not html or not context_dict:
        return html

    # Find all placeholders in the format {placeholder}
    placeholders = re.findall(r'\{([^}]+)\}', html)

    # Replace each placeholder with its value from the context_dict
    result = html
    for placeholder in placeholders:
        if placeholder in context_dict:
            result = result.replace(f"{{{placeholder}}}", str(context_dict[placeholder] or ''))

    return result

