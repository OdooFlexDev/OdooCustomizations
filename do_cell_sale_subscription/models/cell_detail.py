# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CellDetail(models.Model):
    _name = "cell.detail"
    _description = "Cell Detail"
    _order = "create_date desc"
    _check_company_auto = True

    mobile_number = fields.Char(string="Mobile Number", required=True)
    iccid = fields.Char(string="ICCID", required=True)
    cell_type_id = fields.Many2one("cell.type", required=True, string="Cell Type", ondelete="restrict")
    active = fields.Boolean(string="Active", default=True)
    so_line_id = fields.Many2one("sale.order.line", string="Sale Order Line", readonly=True)
    sale_order_id = fields.Many2one("sale.order", related="so_line_id.order_id", string="Sale Order", readonly=True, store=True)
    partner_id = fields.Many2one("res.partner", related="sale_order_id.partner_id", string="Customer", readonly=True,  store=True)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.company)
    
    _sql_constraints = [
        ("mobile_number_unique", "unique(mobile_number)", _("Mobile Number must be unique")),
        ("iccid_unique", "unique(iccid)", _("ICCID must be unique")),
    ]

    @api.depends('mobile_number', 'cell_type_id')
    def _compute_display_name(self):
        for cell in self:
            cell.display_name = f'{cell.mobile_number} - {cell.cell_type_id.name}'

    def unlink(self):
        if self.mapped('so_line_id'):
            raise ValidationError(_("Yup! You can't delete it. It's already linked to Sale/Subscription."))
        return super(CellDetail, self).unlink()

    def action_release_number(self):
        if self.so_line_id:
            self.write({'so_line_id': False})
