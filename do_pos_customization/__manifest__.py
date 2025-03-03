# -*- coding: utf-8 -*-

{
    "name": "DO POS Customization",
    "category": "point_of_sale/fleet",
    "version" : "15.0.0.0.0",
    "summary": "POS Customization and Fleet",
    "description": """POS Customization and Fleet""",
    "author": "Do Incredible",
    "website": "https://doincredible.com",
    "depends": [
        "point_of_sale",
        "fleet"
    ],
    "data": [
        "views/res_partner_views.xml",
        "views/point_of_sale_dashboard.xml",
    ],
    
    "assets": {
        'point_of_sale.assets': [
            "do_pos_customization/static/src/js/models.js",
            "do_pos_customization/static/src/js/ClientDetailsEdit.js",
            'do_pos_customization/static/src/js/ProductScreen.js',
            'do_pos_customization/static/src/js/PaymentScreen.js',
            'do_pos_customization/static/src/js/TicketScreen.js',
        ],
        'web.assets_backend': [
            "do_pos_customization/static/src/js/cash_customer_button.js",
        ],
        'web.assets_qweb': [
            "do_pos_customization/static/src/xml/ClientDetailsEdit.xml",
            "do_pos_customization/static/src/xml/cash_customer_button.xml",
        ],
    },
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
