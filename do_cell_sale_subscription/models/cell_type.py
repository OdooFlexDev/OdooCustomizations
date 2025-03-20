# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CellType(models.Model):
    _name = "cell.type"
    _description = "Cell Type"
    _order = "sequence asc, name asc"
    _check_company_auto = True

    name = fields.Char("Name", required=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)