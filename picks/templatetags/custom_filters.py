from django import template


register = template.Library()


@register.filter
def format_spread(value):
    """
    Custom template filter to format the spread value.
    Adds a plus sign if the value is positive.
    """
    try:
        value = float(value)
        if value > 0:
            return f"+{value}"
        return str(value)
    except (ValueError, TypeError):
        return value

@register.filter
def format_pick_correct(value):
    """
    Custom template filter to return an emoji for correct or incorrect picks.
    """
    try:
        value = bool(value)
        if value == True:
            return "✅"
        else:
            return "❌"
    except (ValueError, TypeError):
        return value

