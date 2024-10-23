from django import template

register = template.Library()


@register.inclusion_tag("base/menu_navbar.html")
def show_menu_navbar(page, path):

    menu = [
        {"name": "home", "display_name": "Home"},
        {"name": "day_page", "display_name": "Day"},
        {"name": "hr_page", "display_name": "Hour"},
        {"name": "smart_buy", "display_name": "Smart Buy"},
        {"name": "trading", "display_name": "Trading"},
        {"name": "configuration", "display_name": "Configuration"},
    ]

    for item in menu:
        if item["name"] == page:
            item["status"] = "active"

    return {"menu": menu}
