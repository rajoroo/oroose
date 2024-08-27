from django import template

register = template.Library()


@register.inclusion_tag("base/menu_navbar.html")
def show_menu_navbar(page, path):

    menu = [
        {"name": "home", "display_name": "Home"},
        {"name": "strong_buy", "display_name": "Strong Buy"},
        {"name": "buy", "display_name": "Buy"},
        {"name": "strong_sell", "display_name": "Strong Sell"},
        {"name": "configuration", "display_name": "Configuration"},
    ]

    for item in menu:
        if item["name"] == page:
            item["status"] = "active"

    return {"menu": menu}
