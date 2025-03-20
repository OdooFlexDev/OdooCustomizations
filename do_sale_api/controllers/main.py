# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request, Response
import json

class SaleOrderController(http.Controller):
    @http.route('/api/get_sale_order', type='json', auth='none', methods=['GET'], csrf=False)
    def get_sale_order(self, **kwargs):
        username = http.request.get_http_params().get('username')
        password = http.request.get_http_params().get('password')

        if not username or not password:
            return {
                "error": "No username and password provided."
            }

        try:
            uid = request.session.authenticate(request.db, username, password)
        except:
            return {
                "error": "Error while login with provided credentials"
            }

        if uid:
            sale_orders = request.env['sale.order'].with_user(uid).search([], limit=10).read()
            return {
                "data": sale_orders
            }
        else:
            return {
                "error": "Login failed. Please provide correct login details"
            }
