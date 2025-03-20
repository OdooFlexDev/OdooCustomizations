# -*- coding: utf-8 -*-
{
    'name': "Do Odoo Notification Sound",

    'summary': "A module to enhance Odoo notifications by managing sound and focus behavior",

    'description': """
    This module customizes Odoo's notification system by adding sound effects and handling focus behavior. 
    It allows you to play sound notifications when specific events occur and ensures the notifications 
    are properly triggered even when the user is not focused on the Odoo application.

    Features:
    - Play customizable sound notifications.
    - Handle audio notifications even if the browser is not in focus.
    - Integrates with Odoo's mail module for event-based notifications.

    This module enhances user experience by ensuring timely and audible alerts for key activities.
    """,

    'author': "Doincredible:Atul",
    'website': "https://doincredible.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    'assets': {
        'web.assets_backend': [
            'do_odoo_notification_sound/static/src/core/web/do_out_of_focus_service_patch.js',
        ],
    },
}
