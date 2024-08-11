from django import template

register = template.Library()


@register.inclusion_tag("base/menu_navbar.html")
def show_menu_navbar(page, path):

    menu = [
        {"name": "home", "display_name": "Home"},
        {"name": "stock_data", "display_name": "Stock Data"},
        {"name": "potential", "display_name": "Potential"},
        {"name": "short_term", "display_name": "Short Term"},
        {"name": "intraday", "display_name": "Intraday"},
        {"name": "trading", "display_name": "Trading"},
        {"name": "trading_monitor", "display_name": "Trading Monitor"},
        {"name": "configuration", "display_name": "Configuration"},
    ]

    for item in menu:
        if item["name"] == page:
            item["status"] = "active"

    return {"menu": menu}
