# -*- coding: utf-8 -*-
{
    'name': "Hide Cancel & Edit Mail Button",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Doincredible",
    'website': "http://www.doincredible.com",

    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','mail','sale'],
    'data': [
        'security/activity_group.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
        (
             "replace",
             "mail/static/src/components/activity/activity.js",
             "do_hide_cancel_edit_mail_button/static/src/components/activity/activity.js",
        )
        ],
        'web.assets_qweb': [
            'do_hide_cancel_edit_mail_button/static/src/components/activity/activity.xml',
        ],
    },
    'license': 'LGPL-3',
}
