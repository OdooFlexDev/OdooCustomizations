# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    def generate_identification_no(self):
        for rec in self:
            rec.identification_id = self.env['ir.sequence'].next_by_code('hr.employee.identification.no')
