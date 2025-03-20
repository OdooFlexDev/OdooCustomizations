# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    cell_ids = fields.Many2many("cell.detail", string="Cells")
    is_cell = fields.Boolean(related="product_id.is_cell", store=True)

    @api.constrains('cell_ids', 'product_uom_qty')
    def _constrains_cell_ids_product_uom_qty(self):
        for line in self:
            if line.product_id and line.product_id.is_cell and line.product_uom_qty > 0 and len(line.cell_ids) != line.product_uom_qty:
                raise UserError(_("Please select cell numbers as specified quantity."))

    def _get_renew_upsell_values(self, subscription_state, period_end=None):
        SOL = self.env['sale.order.line']
        order_lines = super(SaleOrderLine, self)._get_renew_upsell_values(subscription_state, period_end)
        for ol in order_lines:
            parent_line_id = ol[2].get('parent_line_id')
            if parent_line_id:
                ol[2]['cell_ids'] = [(6, [], SOL.browse(parent_line_id).cell_ids.ids)]
        return order_lines

    @api.model_create_multi
    def create(self, vals_list):
        lines = super(SaleOrderLine, self).create(vals_list)
        for line in lines:
            if line.cell_ids:
                line.cell_ids.write({'so_line_id': line.id})
        return lines

    def write(self, vals):
        if 'cell_ids' in vals:
            for line in self:
                line.cell_ids.write({'so_line_id': [(6, [], [])]})
        res = super(SaleOrderLine, self).write(vals)
        for line in self:
            if line.cell_ids:
                line.cell_ids.write({'so_line_id': line.id})
        return res
