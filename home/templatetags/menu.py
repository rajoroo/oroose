from django import template

register = template.Library()


@register.inclusion_tag('base/menu_navbar.html')
def show_menu_navbar(page):

    menu = [
        {"name": "home", "display_name": "Home"},
        {"name": "docs", "display_name": "Docs"},
        {"name": "example", "display_name": "Examples"},
        {"name": "icon", "display_name": "Icons"},
        {"name": "theme", "display_name": "Themes"},
        {"name": "blog", "display_name": "Blog"}
    ]

    for item in menu:
        if item["name"] == page:
            item["status"] = "active"

    return {"menu": menu}
