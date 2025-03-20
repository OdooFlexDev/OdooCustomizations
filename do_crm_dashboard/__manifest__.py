# -*- coding: utf-8 -*-
{
    'name': "Do Crm Dashboard",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Doincredible: Atul",
    'website': "https://doincredible.com/",

    'category': 'tools',
    'version': '0.1',

    'depends': ['crm', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/dashboard_action_menu.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'do_crm_dashboard/static/src/css/style.css',
            'do_crm_dashboard/static/src/js/do_dashboard.js',
            'do_crm_dashboard/static/src/xml/do_dashboard.xml',
        ],
    },


    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}

