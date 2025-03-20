# -*- coding: utf-8 -*-

from odoo import fields, models


class Product(models.Model):
    _inherit = "product.template"

    is_cell = fields.Boolean("Is Cell")
