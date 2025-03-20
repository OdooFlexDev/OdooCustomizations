# -*- coding: utf-8 -*-
{
    'name': "Do Pos Restrict Product Qty",

    'summary': "Pos Restrict Product Qty",

    'description': """
Pos Restrict Product Qty
    """,

    'author': "Do incredible",
    'website': "https://doincredible.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales/Point of Sale',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale', 'hr'],

    'assets': {
        'point_of_sale._assets_pos': [
            'do_pos_restrict_product_qty/static/src/**/*',
        ],
    },
    'installable': True,
    'application': True,
}