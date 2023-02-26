from django import template

register = template.Library()


@register.inclusion_tag("base/menu_navbar.html")
def show_menu_navbar(page):

    menu = [
        {"name": "home", "display_name": "Home"},
        {"name": "bengaluru", "display_name": "Bengaluru"},
        {"name": "mysuru", "display_name": "Mysuru"},
        {"name": "configuration", "display_name": "Configuration"},
        {"name": "data_log", "display_name": "Data Log"},
    ]

    for item in menu:
        if item["name"] == page:
            item["status"] = "active"

    return {"menu": menu}
