from django import template

register = template.Library()


@register.inclusion_tag("base/menu_navbar.html")
def show_menu_navbar(page):

    menu = [
        {"name": "home", "display_name": "Home"},
        {"name": "stoch", "display_name": "STOCH"},
        {"name": "macd", "display_name": "MACD"},
        {"name": "configuration", "display_name": "Configuration"},
    ]

    for item in menu:
        if item["name"] == page:
            item["status"] = "active"

    return {"menu": menu}
