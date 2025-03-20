# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductProduct(models.Model):
    """create new fields in product product model """
    _inherit = 'product.product'

    combo_ok = fields.Boolean('Is Combo', default=False)
    product_combo_ids = fields.One2many('product.combo',
                                        'product_id',
                                        string='Combo')

    @api.model
    def get_combo_data(self, product_id):
        """create a function to get combo data"""
        product = self.env['product.product'].browse(product_id)
        combo_data = []

        for combo in product.product_combo_ids:
            combo_values = {
                'pos_category_id': combo.pos_category_id.id,
                'pos_category_name': combo.pos_category_id.name,
                'product_img': [],
                'product_ids': [],
                'product_names': [],
                'is_required': combo.is_required,
                'item_count': combo.item_count,
            }
            # Loop through the product_ids of the combo item
            for product_item in combo.product_ids:
                combo_values['product_ids'].append(product_item.id)
                combo_values['product_names'].append(product_item.name)
                combo_values['product_img'].append(product_item.image_1920)
            combo_data.append(combo_values)
        return combo_data
