# -*- coding: utf-8 -*-
{
    'name': "Do Change Effective Date",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Doincredible",
    'website': "https://doincredible.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Inventory/Inventory',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web','purchase', 'stock', 'account_invoice_extract', 'account','sale_management', 'mrp_account', 'mrp'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/res_group.xml',
        'wizard/date_wizard.xml',
    ],
    'installable': True,
    'application': True,
}

