from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def execute_button(self, *args, **kwargs):
        return args, kwargs
