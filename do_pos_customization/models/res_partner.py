# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    fleet_id = fields.Many2one("fleet.vehicle", string="Fleet")