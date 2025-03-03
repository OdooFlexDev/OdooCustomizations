# -*- coding: utf-8 -*-
{
    'name': "Do Generate Id No",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','hr'],

    'data': [
        'data/ir_sequence.xml',
        'views/views.xml',
    ],

}
