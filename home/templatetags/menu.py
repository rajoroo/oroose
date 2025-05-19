from django import template

register = template.Library()


@register.inclusion_tag("base/menu_navbar.html")
def show_menu_navbar(page, path):

    menu = [
        {"name": "home", "display_name": "Home"},
        {"name": "week_page", "display_name": "Week"},
        {"name": "day_page", "display_name": "Day"},
        {"name": "hr_page", "display_name": "Hour"},
        {"name": "potential_page", "display_name": "Potential"},
        {"name": "stoch_page", "display_name": "Stoch"},
        {"name": "rsi_page", "display_name": "RSI"},
        {"name": "trading", "display_name": "Trading"},
        {"name": "configuration", "display_name": "Configuration"},
    ]

    for item in menu:
        if item["name"] == page:
            item["status"] = "active"

    return {"menu": menu}
