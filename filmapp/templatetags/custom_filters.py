from django import template
import re

register = template.Library()

@register.filter
def slice_and_ellipsis(value, length):
    if len(value) <= length:
        return value
    else:
        truncated_text = value[:length]
        last_space_index = re.search(r'[\s.,!?;]', truncated_text[::-1]).start()
        if last_space_index:
            return truncated_text[:-last_space_index] + '...'
        else:
            return truncated_text + '...'
