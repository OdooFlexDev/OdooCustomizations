# -*- coding: utf-8 -*-

from odoo import models, fields, _

class PosSession(models.Model):
    _inherit = 'pos.session'

    def get_closing_control_data(self):
        if not self.env.user.has_group('point_of_sale.group_pos_user'):
            raise AccessError(_("You don't have the access rights to get the point of sale closing control data."))
        
        self.ensure_one()

        orders = self.order_ids.filtered(lambda o: o.state in ('paid', 'invoiced'))
        payments = orders.payment_ids.filtered(lambda p: p.payment_method_id.type != "pay_later")
        pay_later_payments = orders.payment_ids - payments

        cash_payment_method_ids = self.payment_method_ids.filtered(lambda pm: pm.type == 'cash')
        default_cash_payment_method_id = cash_payment_method_ids[0] if len(cash_payment_method_ids) > 0 else None
        cash2_payment_method_id = cash_payment_method_ids[1] if len(cash_payment_method_ids) > 1 else None
        cash3_payment_method_id = cash_payment_method_ids[2] if len(cash_payment_method_ids) > 2 else None
        def total_payment_amount(payment_method_id):
            return sum(payments.filtered(lambda p: p.payment_method_id == payment_method_id).mapped('amount'))

        total_default_cash_payment_amount = total_payment_amount(default_cash_payment_method_id)
        total_cash2_payment_amount = total_payment_amount(cash2_payment_method_id)
        total_cash3_payment_amount = total_payment_amount(cash3_payment_method_id)

        other_payment_method_ids = self.payment_method_ids - cash_payment_method_ids

        cash_in_out_list = []
        cash_in_count = 0
        cash_out_count = 0

        for cash_move in self.sudo().cash_register_id.line_ids.sorted('create_date'):
            if cash_move.amount > 0:
                cash_in_count += 1
                name = f'Cash in {cash_in_count}'
            else:
                cash_out_count += 1
                name = f'Cash out {cash_out_count}'
            cash_in_out_list.append({
                'name': cash_move.payment_ref or name,
                'amount': cash_move.amount
            })

        def get_cash_details(payment_method_id, total_payment_amount):
            return {
                'name': payment_method_id.name,
                'amount': self.cash_register_id.balance_start + total_payment_amount + sum(self.sudo().cash_register_id.line_ids.mapped('amount')),
                'opening': self.cash_register_id.balance_start,
                'payment_amount': total_payment_amount,
                'moves': cash_in_out_list,
                'id': payment_method_id.id
            } if payment_method_id else None

        return {
            'orders_details': {
                'quantity': len(orders),
                'amount': sum(orders.mapped('amount_total'))
            },
            'payments_amount': sum(payments.mapped('amount')),
            'pay_later_amount': sum(pay_later_payments.mapped('amount')),
            'opening_notes': self.opening_notes,
            'default_cash_details': get_cash_details(default_cash_payment_method_id, total_default_cash_payment_amount),
            'cash2_details': get_cash_details(cash2_payment_method_id, total_cash2_payment_amount),
            'cash3_details': get_cash_details(cash3_payment_method_id, total_cash3_payment_amount),
            'other_payment_methods': [{
                'name': pm.name,
                'amount': sum(orders.payment_ids.filtered(lambda p: p.payment_method_id == pm).mapped('amount')),
                'number': len(orders.payment_ids.filtered(lambda p: p.payment_method_id == pm)),
                'id': pm.id,
                'type': pm.type,
            } for pm in other_payment_method_ids],
            'is_manager': self.user_has_groups("point_of_sale.group_pos_manager"),
            'amount_authorized_diff': self.config_id.amount_authorized_diff if self.config_id.set_maximum_difference else None
        }


    def action_pos_session_closing_control(self, balancing_account=False, amount_to_balance=0, bank_payment_method_diffs=None):
        bank_payment_method_diffs = bank_payment_method_diffs or {}
        self._check_pos_session_balance()
        for session in self:
            if any(order.state == 'draft' for order in session.order_ids):
                raise UserError(_("You cannot close the POS when orders are still in draft"))
            if session.state == 'closed':
                raise UserError(_('This session is already closed.'))
            session.write({'state': 'closing_control', 'stop_at': fields.Datetime.now()})
            if not session.config_id.cash_control:
                return session.action_pos_session_close(balancing_account, amount_to_balance, bank_payment_method_diffs)
            # If the session is in rescue, we only compute the payments in the cash register
            # It is not yet possible to close a rescue session through the front end, see `close_session_from_ui`
            if session.rescue and session.config_id.cash_control:
                cash_payment_method_ids = self.payment_method_ids.filtered(lambda pm: pm.type == 'cash')
                orders = self.order_ids.filtered(lambda o: o.state == 'paid' or o.state == 'invoiced')
                total_cash = sum(
                    orders.payment_ids.filtered(lambda p: p.payment_method_id in cash_payment_method_ids).mapped('amount')
                ) + self.cash_register_balance_start

                session.cash_register_id.balance_end_real = total_cash
            return session.action_pos_session_validate(balancing_account, amount_to_balance, bank_payment_method_diffs)
