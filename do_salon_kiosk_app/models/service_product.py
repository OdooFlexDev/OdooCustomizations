# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    duration = fields.Integer(string="Duration (minutes)")
    salon_ok = fields.Boolean()
    pre_service = fields.Char("Pre Service")
    post_service = fields.Char("Post Service")
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    duration = fields.Integer(string="Duration (minutes)")

class AccountMove(models.Model):
    _inherit = 'account.move'

    salon_id = fields.Many2one('salon.client.checkin')