from django import template

register = template.Library()


@register.inclusion_tag("base/menu_navbar.html")
def show_menu_navbar(page, path):

    menu = [
        {"name": "home", "display_name": "Home", "path": None, "has_path": False},
        {"name": "configuration", "display_name": "Configuration", "path": None, "has_path": False},
    ]

    for item in menu:
        if item["name"] == page and item["path"] == path:
            item["status"] = "active"

    return {"menu": menu}
