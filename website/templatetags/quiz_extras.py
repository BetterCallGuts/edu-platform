from django import template

register = template.Library()

@register.filter
def get_option(question, opt_num):
    """
    Fetch the option text for a question dynamically.
    Usage: {{ question|get_option:"1" }}
    """
    # Map numbers to the correct fields
    field_map = {
        "1": "get_question_1",
        "2": "get_question_2",
        "3": "get_question_3",
        "4": "get_question_4",
    }

    field_name = field_map.get(str(opt_num))
    if not field_name:
        return ""

    # Call the method/property safely
    if hasattr(question, field_name):
        field = getattr(question, field_name)
        return field() if callable(field) else field

    return ""
