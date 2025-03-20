# -*- coding: utf-8 -*-
{
    'name': "Do Employee Po Access",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "DoIncredible",
    'website': "https://doincredible.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','hr', 'account','web','purchase','sale_management'],

    # always loaded
    'data': [
        'security/security_group.xml',
        'views/views.xml',
        'views/webclient_views.xml',
    ],

}

