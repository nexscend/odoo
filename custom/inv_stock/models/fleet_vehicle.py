# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model_create_multi
    def create(self, vals_list):
        configs = super().create(vals_list)
        return configs