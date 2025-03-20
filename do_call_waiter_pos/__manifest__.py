# -*- encoding: utf-8 -*-

{
	'name': "Call Waiter Notification In Restaurant Screen",
	'category': 'Extra',
	'author': 'Inkal Patel',
	'license': 'OPL-1',
	'summary': "Call Waiter Notification In Restaurant Screen",
	'website': 'https://doincredible.com',
	'version': '1.0',
	'description': """
		Call Waiter Notification In Restaurant Screen
	""",
	'depends': ['base','pos_self_order','point_of_sale'],
	'data': [
	],
	"assets": {
		"pos_self_order.assets": [
			"do_call_waiter_pos/static/src/xml/order_widget.xml",
			"do_call_waiter_pos/static/src/js/order_widget.js",
		],
		'point_of_sale._assets_pos': [
			"do_call_waiter_pos/static/src/js/floor_screen.js",
		],
	},
	'installable': True,
	'auto_install': False,
}