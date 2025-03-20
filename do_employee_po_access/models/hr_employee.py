# -*- coding: utf-8 -*-

from odoo import api, fields, models
from lxml import etree

class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        # Get the current user
        user = self.env.user
        if user.has_group('do_employee_po_access.group_own_employee'):
            if domain:
                domain = ['|', ('user_id', '=', user.id), ('create_uid', '=', user.id)] + domain
            else:
                domain = ['|', ('user_id', '=', user.id), ('create_uid', '=', user.id)]     
        return super()._search(domain, offset, limit, order, access_rights_uid)

    @api.model
    def get_view(self, view_id=None, view_type='form', **options):
        res = super().get_view(view_id, view_type, **options)
        
        if view_type == 'form' and self.env.user.has_group('do_employee_po_access.group_own_employee'):
            arch = etree.fromstring(res['arch'])
            for node in arch.xpath("//form"):
                node.set('create', '0')
            res['arch'] = etree.tostring(arch, pretty_print=True).decode('utf-8')
        
        elif view_type == 'tree' and self.env.user.has_group('do_employee_po_access.group_own_employee'):
            arch = etree.fromstring(res['arch'])
            for node in arch.xpath("//tree"):
                node.set('create', '0')
            res['arch'] = etree.tostring(arch, pretty_print=True).decode('utf-8')

        elif view_type == 'kanban' and self.env.user.has_group('do_employee_po_access.group_own_employee'):
            arch = etree.fromstring(res['arch'])
            for node in arch.xpath("//kanban"):
                node.set('create', '0')
            res['arch'] = etree.tostring(arch, pretty_print=True).decode('utf-8')
        
        return res

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    partner_id = fields.Many2one('res.partner', domain=lambda self: self._get_partner_id_domain(), string='Vendor', required=True, change_default=True, tracking=True, check_company=True, help="You can find a vendor by its Name, TIN, Email or Internal Reference.")

    def _get_partner_id_domain(self):
        user = self.env.user
        if user.allowed_vendor_ids:
            return [('id', 'in', user.allowed_vendor_ids.ids)]
        else:
            return []


    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        user = self.env.user
        if user.has_group('do_employee_po_access.group_own_purchase'):
            domain = ['|', ('user_id', '=', user.id), ('create_uid', '=', user.id)] + domain
            if user.allowed_vendor_ids:
                domain = ['&', ('partner_id', 'in', user.allowed_vendor_ids.ids)] + domain
        return super(PurchaseOrder, self)._search(domain, offset, limit, order, access_rights_uid)


class AccountMOve(models.Model):
    _inherit = 'account.move'


    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
        user = self.env.user
        if user.has_group('do_employee_po_access.group_own_move'):
            if domain:
                domain = ['|', ('partner_id', 'in', user.allowed_vendor_ids.ids), ('create_uid', '=', user.id)] + domain
            else:
                domain = ['|', ('partner_id', 'in', user.allowed_vendor_ids.ids), ('create_uid', '=', user.id)]    
        return super()._search(domain, offset, limit, order, access_rights_uid)
       
