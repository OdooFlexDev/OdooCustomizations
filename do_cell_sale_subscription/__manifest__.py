# -*- coding: utf-8 -*-

{
    "name": "Cell Management",
    "author": "Do Incredible",
    "website": "https://doincredible.com",
    "version": "17.0.0.0",
    "category": "Sales",
    "summary": "Manage Cell Details",
    "description": "This module adds a new model for cell details and integrates it with sales orders/subscriptions.",
    "depends": [
        "sale_subscription"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/cell_detail_views.xml",
        "views/cell_type_views.xml",
        "views/product_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "icon": "do_cell_sale_subscription/static/description/icon.png",
    "license": "LGPL-3",
}
