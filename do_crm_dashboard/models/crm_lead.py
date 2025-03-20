# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.safe_eval import datetime
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import calendar

def get_period_start_date(period):
    """Returns the start date for the given period"""
    today = datetime.datetime.now()

    if period == 'month':
        start_date = today.replace(day=1)
    elif period == 'quarter':
        current_month = today.month
        start_month = ((current_month - 1) // 3) * 3 + 1
        start_date = today.replace(month=start_month, day=1)
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
    elif period == 'week':
        start_date = today - datetime.timedelta(days=today.weekday())
    else:
        raise ValueError("Invalid period specified")

    return start_date.date()

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    @api.model
    def get_upcoming_events(self, time):
        """Upcoming Activities Table"""
        date = get_period_start_date(time)
        session_user_id = self.env.uid
        
        # Search for the activities related to the CRM leads
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'crm.lead'),
            ('date_deadline', '>=', date),
            ('user_id', '=', session_user_id)
        ], order='date_deadline asc')
        
        # Prepare the events data
        events = []
        for activity in activities:
            # print("==activity===\n\n",activity.body)
            activity_type_name = activity.activity_type_id.name if activity.activity_type_id else ''
            user_name = activity.user_id.name if activity.user_id else ''
            events.append([
                activity.activity_type_id.id,
                activity.date_deadline,
                activity.summary,
                activity.res_name,
                activity_type_name,
                user_name
            ])
        return {
            'event': events,
            'cur_lang': self.env.context.get('lang')
        }


    @api.model
    def get_crm_data(self, time):
        date = get_period_start_date(time)
        company_id = self.env.company
        leads = self.search([('company_id', '=', company_id.id), 
                             ('user_id', '=', self.env.user.id),
                             ('create_date', '>=', date)])

        # Filter leads and opportunities in a more efficient way
        my_leads = leads.filtered(lambda r: r.type == 'lead')
        my_opportunities = leads.filtered(lambda r: r.type == 'opportunity')

        # Filter won opportunities
        won_opportunities = my_opportunities.filtered(lambda r: r.stage_id.is_won)

        # Get the company currency symbol
        currency = company_id.currency_id.symbol
        
        # Calculate expected revenue and actual revenue from won opportunities
        expected_revenue = sum(my_opportunities.mapped('expected_revenue'))
        revenue = sum(won_opportunities.mapped('expected_revenue'))

        # Total customer count (won opportunities)

        # total_customer = len(won_opportunities)

        total_customer = len(self.env['res.partner'].search([]))
        
        # Active customers (with ongoing opportunities)
        active_customer = len(my_opportunities.filtered(lambda r: not r.stage_id.is_won))

        # Count leads with active status and probability conditions
        active_lead_count = len(leads.filtered(lambda r: r.active and r.probability == 0))
        win_count = len(leads.filtered(lambda r: r.active and r.probability == 100))

        # Calculate win ratio
        win_ratio = win_count / active_lead_count if active_lead_count else 0
        opportunity_ratio = len(won_opportunities) / len(my_opportunities) if len(my_opportunities) else 0

        # Return the data
        return {
            'total_leads': len(my_leads),
            'total_opportunity': len(my_opportunities),
            'win_ratio': win_ratio,
            'opportunity_ratio':opportunity_ratio,
            'revenue': revenue,
            'currency': currency,
            'expected_revenue': expected_revenue,
            'total_customer': total_customer,
            'active_customer': active_customer,
        }

    @api.model
    def get_top_salesperson_revenue(self, time):
        """Top 10 Salesperson revenue Table"""
        # session_user_id = self.env.uid
        date = get_period_start_date(time)
        leads = self.env['crm.lead'].search([
            ('expected_revenue', '!=', False),
            ('user_id', '!=', False),
            ('create_date', '>=', date)
        ], order='expected_revenue DESC', limit=10)

        top_revenue = [
            [lead.user_id.name, lead.id, lead.expected_revenue, lead.name,
             lead.company_id.currency_id.symbol,lead.team_id.name,lead.team_id.invoiced_target] for lead in leads
        ]
        
        return {'top_revenue': top_revenue}


    @api.model
    def get_monthly_sales(self):
        from datetime import datetime
        current_year = datetime.today().year

        sale_orders = self.env['sale.order'].search([
            ('date_order', '>=', f'{current_year}-01-01'),
            ('date_order', '<=', f'{current_year}-12-31')
        ])

        monthly_sales = {i: 0 for i in range(1, 13)}

        for order in sale_orders:
            order_month = order.date_order.month
            monthly_sales[order_month] += order.amount_total
        return monthly_sales



    @api.model
    def get_forcasted_monthly_sales(self):
        company_id = self.env.company
        today = fields.Date.today()
        current_month = today.month
        current_year = today.year

        leads = self.with_context(
            forecast_filter=True
        ).search([
            ('company_id', '=', company_id.id),
            ('user_id', '=', self.env.user.id),
            ('date_deadline', '>=', today),
            ('type', '=', 'opportunity')
        ])
        leads = leads.filtered(lambda l: l.active)

        month_wise_revenue = defaultdict(float)

        for lead in leads:
            if lead.date_deadline.month > current_month and lead.date_deadline.year == current_year:
                month_key = lead.date_deadline.strftime('%Y-%m')
                month_wise_revenue[month_key] += lead.expected_revenue or 0

        month_wise_revenue = dict(month_wise_revenue)

        return month_wise_revenue



    @api.model
    def get_lead_by_campaign(self):
        """Leads Group By Campaign"""
        start_date = fields.Date.today()
        
        # Search for leads created after the start date and that have a campaign_id
        leads = self.search([('create_date', '<=', start_date), ('campaign_id', '!=', False)])
        
        # Group the leads by campaign_id and count the number of occurrences
        campaign_counts = {}
        for lead in leads:
            campaign_id = lead.campaign_id.id
            if campaign_id not in campaign_counts:
                campaign_counts[campaign_id] = 0
            campaign_counts[campaign_id] += 1
        
        # Fetch the names of the campaigns
        campaigns = self.env['utm.campaign'].browse(campaign_counts.keys())
        campaign_names = {campaign.id: campaign.name for campaign in campaigns}

        # Prepare the final output
        counts = list(campaign_counts.values())
        names = [campaign_names[campaign_id] for campaign_id in campaign_counts.keys()]
        return [counts, names]


