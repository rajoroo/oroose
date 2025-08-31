from django import template

register = template.Library()


@register.inclusion_tag("base/menu_navbar.html")
def show_menu_navbar(page, path):

    menu = [
        {"name": "week_page", "icon": "fas fa-calendar-week", "display_name": "Week"},
        {"name": "day_page", "icon": "fas fa-calendar-day", "display_name": "Day"},
        {"name": "potential_page", "icon": "fas fa-th-list", "display_name": "Potential"},
        {"name": "heikinashi_page", "icon": "fas fa-chart-bar", "display_name": "Heikin-Ashi"},
        {"name": "stochastic_page", "icon": "fas fa-chart-line", "display_name": "Stochastic"},
        {"name": "configuration", "icon": "fas fa-toolbox", "display_name": "Configuration"},
    ]

    for item in menu:
        if item["name"] == page:
            item["status"] = "active"

    return {"menu": menu}
