from django import template

register = template.Library()


@register.filter
def get_pick_for_week(picks, week):
    """
    Custom template filter to get the pick for a specific week.
    """
    try:
        return picks.get(week=week).team
    except picks.model.DoesNotExist:
        return 'No Pick'


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
