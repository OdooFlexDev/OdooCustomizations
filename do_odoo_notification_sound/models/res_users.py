from odoo import models, fields

class ResUsers(models.Model):
    _inherit='res.users'

    notify_message = fields.Char("Notify Message")

    def get_userdata(self,id):
        print("==id==\n\n\n\n",id)
        pass