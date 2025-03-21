# -*- coding: utf-8 -*-

from odoo import models, fields

class Meeting(models.Model):
    _inherit = 'calendar.event'

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    contact_id = fields.Many2one("res.partner", string="Contact")
    partner_id = fields.Many2one(
        'res.partner', string='Scheduled by', related='contact_id', readonly=True)

    flag = fields.Boolean(compute='check_group')

    def check_group(self):
        if self.user_has_groups('appointment.group_appointment_agent'):
            self.flag = True
        else:
            self.flag = False