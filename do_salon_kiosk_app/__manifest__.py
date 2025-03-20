# -*- coding: utf-8 -*-
{
    'name': "Do Salon Kiosk App",

    'summary': "Salon kiosk module",

    'description': """
Long description of module's purpose
    """,

    'author': "Do Incredible: Atul Patel",
    'website': "https://doincredible.com/",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'web', 'product', 'account'],

    'data': [
        'security/ir.model.access.csv',
        'data/salon_sequence.xml',
        'views/client_ckeckin.xml',
        'views/salon_service.xml',
        'views/salon_kiosk.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'do_salon_kiosk_app/static/src/**/*',
        ],
  
    },
    'module_type': 'official',
    'installable': True,
    'application': True,
}

