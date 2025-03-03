# -*- coding: utf-8 -*-
{
    'name': "Do Split Odoo Window",
    'summary': """Dual-view layout, seamlessly dividing the screen into list and detail sections for CRUD operations.""",
    'author': "Do Incredible",
    'license': 'LGPL-3',
    'category': 'Technical',
    'version': '15.0.0',
    'price': 139.36,
    'currency': 'EUR',
    'depends': ['base', 'web', 'web_editor', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/create_view_split_wizard.xml',
        'views/split_view.xml',
    ],
    
    "images": ['static/description/banner.png'],
    'assets': {
        'website.assets_wysiwyg': [
            'do_split_odoo_window/static/src/js/fix_wysiwyg.js',
        ],
        'web.assets_qweb': [
            'do_split_odoo_window/static/src/xml/**/*',
        ],
        'web.assets_backend': [
            'do_split_odoo_window/static/src/scss/split_view.scss',
            'do_split_odoo_window/static/src/js/split_listview.js',
            'do_split_odoo_window/static/src/js/split_formview.js',
            'do_split_odoo_window/static/src/js/split_view.js',
            'do_split_odoo_window/static/src/js/debug_items.js',
        ],
    },
    'uninstall_hook': '_uninstall_hook',

}
