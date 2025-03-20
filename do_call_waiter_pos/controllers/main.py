# -*- coding: utf-8 -*-
import re
from datetime import timedelta
from odoo import http, fields
from odoo.http import request
from odoo.tools import float_round
from werkzeug.exceptions import NotFound, BadRequest, Unauthorized

class PosSelfOrderController(http.Controller):

	@http.route("/set/active_tables/", auth="public", type="json", website=True)
	def set_active_tables(self, **kwargs):
		floor_id = kwargs.get("floor_id")
		table = kwargs.get("table")
		if floor_id and table:
			floor_id = request.env['restaurant.floor'].browse(int(floor_id))
			floor_id.set_active_tables(table,"remove",{})
		return {}

	@http.route("/check/active_tables/", auth="public", type="json", website=True)
	def check_active_tables(self, **kwargs):
		floor_id = kwargs.get("floor_id")
		table = kwargs.get("table")
		if floor_id and table:
			floor_id = request.env['restaurant.floor'].browse(int(floor_id))
			active_tables = floor_id.set_active_tables(table,"",{})
			if str(table) in active_tables.keys():
				return {"data":True}
		return {"data":False}