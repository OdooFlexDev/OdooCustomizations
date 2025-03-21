# -*- coding: utf-8 -*-
{
    'name': "Do Calendar Event Access Right",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Do incredible:Atul",
    'website': "https://doincredible.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','calendar','appointment'],

    # always loaded
    'data': [
        'security/security_rule.xml',
        'views/views.xml',
    ],

}

