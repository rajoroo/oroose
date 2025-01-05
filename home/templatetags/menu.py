from django import template

register = template.Library()


@register.inclusion_tag("base/menu_navbar.html")
def show_menu_navbar(page, path):

    menu = [
        {"name": "home", "display_name": "Home"},
        {"name": "week_page", "display_name": "Week"},
        {"name": "day_page", "display_name": "Day"},
        {"name": "smart_buy_page", "display_name": "Smart Buy"},
        {"name": "week_level_0_to_20_page", "display_name": "Week Level 0 to 20"},
        {"name": "week_level_20_to_50_page", "display_name": "Week Level 20 to 50"},
        {"name": "week_level_50_to_80_page", "display_name": "Week Level 50 to 80"},
        {"name": "trading", "display_name": "Trading"},
        {"name": "configuration", "display_name": "Configuration"},
    ]

    for item in menu:
        if item["name"] == page:
            item["status"] = "active"

    return {"menu": menu}
