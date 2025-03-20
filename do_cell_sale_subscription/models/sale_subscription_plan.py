# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SaleSubscriptionPlan(models.Model):
    _inherit = 'sale.subscription.plan'

    billing_period_unit = fields.Selection(selection_add=[("day", "Days")], ondelete={'day': 'set default'})

