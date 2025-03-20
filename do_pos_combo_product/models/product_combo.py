# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductCombo(models.Model):
    """create a new model product combo"""
    _name = 'product.combo'

    pos_category_id = fields.Many2one('pos.category',
                                      string='Category')
    product_ids = fields.Many2many('product.product',
                                   string='Products')
    is_required = fields.Boolean(string='Is Required')
    item_count = fields.Integer(string='Item Count')
    product_id = fields.Many2one('product.product',
                                 string='product')
