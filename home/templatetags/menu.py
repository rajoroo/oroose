from django import template

register = template.Library()


@register.inclusion_tag("base/menu_navbar.html")
def show_menu_navbar(page):

    menu = [
        {"name": "home", "display_name": "Home"},
        {"name": "stoch_daily", "display_name": "STOCH DAILY"},
        {"name": "stoch_weekly", "display_name": "STOCH WEEKLY"},
        {"name": "potential_stock", "display_name": "Potential Stock"},
        {"name": "short_term", "display_name": "Short Term"},
        {"name": "configuration", "display_name": "Configuration"},
    ]

    for item in menu:
        if item["name"] == page:
            item["status"] = "active"

    return {"menu": menu}
