# -*- coding: utf-8 -*-

{
    "name": "DO POS Cash Payment",
    "category": "point_of_sale",
    "version" : "15.0.0.0.0",
    "summary": "POS Cash Payment",
    "description": """DO POS Multi Cash Payment""",
    "author": "Do Incredible",
    "website": "https://doincredible.com",
    "depends": [
        "point_of_sale",
    ],
    
    "assets": {
        'point_of_sale.assets': [
            "do_pos_cash_payment/static/src/js/models.js",
            "do_pos_cash_payment/static/src/js/ClosePosPopups.js",
        ],
        'web.assets_qweb': [
            "do_pos_cash_payment/static/src/xml/ClosePosPopups.xml",
        ],
    },
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
