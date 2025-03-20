# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import re

class ClientCheckIn(models.Model):
    _name = 'salon.client.checkin'
    _description = 'Client Check-In'
    _order = 'checkin_date asc'

    name = fields.Char(
        'Service Reference',
        default=lambda self: self.env['ir.sequence'].next_by_code('salon.client.checkin') or '',
        required=True)
    partner_id = fields.Many2one("res.partner", string="Client Name", required=True)
    phone = fields.Char(related="partner_id.phone", string="Phone Number", required=True)
    email = fields.Char(related="partner_id.email", string="Email")
    service_ids = fields.Many2many('product.product', string="Service", required=True, domain=[('salon_ok','=', True)])
    terms_accepted = fields.Boolean(string="Agreed to Terms and Conditions", required=True)
    checkin_date = fields.Datetime(string="Check-In Date", default=fields.Datetime.now)
    waiting_time = fields.Char("Waiting time (minutes)", compute="_compute_waiting_time")
    state = fields.Selection([
        ('waiting', 'Waiting'),
        ('in_service', 'In Service'),
        ('completed', 'Completed'),
        ('invoiced', 'Invoiced')
    ], default='waiting')
    move_id = fields.Many2one('account.move')
    
    def SendMessage(self):
        pass

    @api.depends('checkin_date', 'state')
    def _compute_waiting_time(self):
        for record in self:
            total_duration = 0
            if record.checkin_date and record.state == 'waiting':
                previous_checkins = self.env['salon.client.checkin'].search([
                    ('checkin_date', '<', record.checkin_date),
                    ('state', 'in', ['waiting', 'in_service']),
                ]) - self
                for checkin in previous_checkins:
                    if checkin.service_ids:
                        total_duration += sum(checkin.service_ids.mapped('duration'))
            record.waiting_time = total_duration


    def action_create_invoice(self):
        # Ensure the check-in is completed before generating the invoice
        if self.state != 'completed':
            raise UserError("The client check-in must be completed before generating an invoice.")
        
        invoice_vals = {
            'partner_id': self.partner_id.id,
            'invoice_date': fields.Date.today(),
            'move_type': 'out_invoice',
            'invoice_line_ids': [],
            'salon_id': self.id,
        }
        notes = ''
        invoice_line_vals = []
        for service in self.service_ids:
            invoice_line_vals.append((0, 0, {
                'product_id': service.id,
                'name': service.name,
                'quantity': 1,
                'price_unit': service.lst_price,
            }))
            notes += service.description if service.description else ''
        
        invoice_vals['invoice_line_ids'] = invoice_line_vals
        invoice_vals['narration'] = notes
        invoice = self.env['account.move'].create(invoice_vals)
        invoice.action_post()
        self.write({'state':'invoiced'})
        return invoice


    def action_view_invoice(self):
        self.ensure_one()
        result = {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "domain": [('salon_id', '=', self.id)],
            "context": {"create": False},
            "name": _("Customer Invoice"),
            'view_mode': 'tree,form',
        }
        return result


    @api.model
    def search_and_create(self, name, phone, email, service_ids, terms_accepted):
        existing_client = self.env['res.partner'].search(['|',('phone', '=', phone), ('email', '=', email)], limit=1)
        service_ids = self.env['product.product'].browse(service_ids)
        if existing_client:
            checkin = self.create({
                'partner_id': existing_client.id,
                'service_ids': service_ids.ids,
                'terms_accepted': terms_accepted,
                'checkin_date': fields.Datetime.now(),
            })
            return checkin.name, checkin.waiting_time
        else:
            client = self.env['res.partner'].create({
                'name': name,
                'phone': phone,
                'email': email,
            })
            checkin = self.create({
                'partner_id': client.id,
                'service_ids': service_ids.ids,
                'terms_accepted': terms_accepted,
                'checkin_date': fields.Datetime.now(),
            })
            return checkin.name, checkin.waiting_time


    @api.constrains('terms_accepted')
    def _check_terms(self):
        for record in self:
            if not record.terms_accepted:
                raise ValidationError("You must agree to the terms and conditions to proceed.")

    @api.constrains('phone')
    def _check_phone(self):
        for record in self:
            phone_pattern = r'^\+?[1-9]\d{7,14}$'
            if not re.match(phone_pattern, record.phone):
                raise ValidationError("Please enter a valid phone number.")

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if record.email and not re.match(email_pattern, record.email):
                raise ValidationError("Please enter a valid email address.")
   
    def action_confirm(self):
        self.write({'state': 'in_service'})

    def set_to_draft(self):
        self.write({'state': 'waiting'})

    def action_done(self):
        self.write({'state': 'completed'})