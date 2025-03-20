import json
from odoo import http
from odoo.http import request
from collections import defaultdict

class CApiController(http.Controller):
    @http.route('/api/get_crm_data', type='http', auth='public', methods=['GET'], csrf=False)
    def get_crm_data(self, **kwargs):
        leads = request.env['crm.lead'].sudo().search([], limit=20)
        if not leads.exists():
            return json.dumps({'status': 'error', 'message': 'Lead not found'})

        data_list = []
        for lead in leads:
            data = {
                'id': lead.id,
                'name': lead.contact_name or '',
                'email': lead.email_from or '',
                'company': lead.partner_name or '',
                'title': lead.title.name if lead.title else '',
                'status': lead.stage_id.name if lead.stage_id else 'New',
            }
            data_list.append(data)

        response = request.make_response(
            json.dumps(data_list),
            headers={
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://192.168.29.55:5173',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            }
        )
        return response

    @http.route('/api/CRM/v1/dealsign', type='http', auth='public', methods=['GET'], csrf=False)
    def get_dealsigninformation(self, **kwargs):
        won_stages = request.env['crm.stage'].search([('is_won', '=', True)]).ids
        
        deals_aggregate = defaultdict(lambda: defaultdict(float))

        leads = request.env['crm.lead'].sudo().search(
            ['|', ('stage_id', 'in', won_stages), ('active', '=', False)],
        )
        for lead in leads:
            close_date = lead.date_closed
            month = close_date.month
            year = close_date.year
            stage_title = "WON" if lead.active else "LOST"
            deal_value = lead.expected_revenue

            deals_aggregate[stage_title][(month, year)] += deal_value

        result = {
            "data": {
                "dealStages": {
                    "nodes": []
                }
            }
        }

        for stage in ['WON', 'LOST']:
            deals_for_stage = []
            for (month, year), total in deals_aggregate[stage].items():
                deals_for_stage.append({
                    "groupBy": {
                        "closeDateMonth": month,
                        "closeDateYear": year
                    },
                    "sum": {
                        "value": total
                    }
                })
            
            result['data']['dealStages']['nodes'].append({
                "title": stage,
                "dealsAggregate": deals_for_stage
            })
        
        response = request.make_response(
            json.dumps(result),
            headers={
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': 'http://192.168.29.55:5173',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            }
        )
        return response