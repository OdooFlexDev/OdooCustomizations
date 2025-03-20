# -*- coding: utf-8 -*-

from odoo import api, fields, models, _, Command
import json

class RestaurantFloor(models.Model):
	_inherit = 'restaurant.floor'

	name = fields.Char('Floor Name', required=True)
	pos_config_ids = fields.Many2many('pos.config', string='Point of Sales', domain="[('module_pos_restaurant', '=', True)]")
	background_image = fields.Binary('Background Image')
	background_color = fields.Char('Background Color', help='The background color of the floor in a html-compatible format', default='rgb(249,250,251)')
	table_ids = fields.One2many('restaurant.table', 'floor_id', string='Tables')
	sequence = fields.Integer('Sequence', default=1)
	active = fields.Boolean(default=True)
	floor_background_image = fields.Image(string='Floor Background Image')
	active_tables = fields.Char("Active Tables")

	def set_active_tables(self,table,op_type,data):
		if op_type == "add":
			active_tables_dict = json.loads(self.active_tables) if self.active_tables else {}
			if not active_tables_dict.get(table):
				active_tables_dict.update({table: data})
			self.active_tables = json.dumps(active_tables_dict)
		elif op_type == "remove" and self.active_tables and table:
			active_tables_dict = json.loads(self.active_tables)
			del active_tables_dict[table]
			self.active_tables = json.dumps(active_tables_dict)
		else:
			return json.loads(self.active_tables) if self.active_tables else {}